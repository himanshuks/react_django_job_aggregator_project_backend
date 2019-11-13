from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from knox.auth import TokenAuthentication

from .serializers import NewTransactionSerializer
from .utils import generate_client_token, find_transaction, transact
from .models import PaymentDetail, Transaction

from subscriptionplans.models import UserSubscriptionPlan, SubscriptionPlan
# Create your views here.


# Old
@login_required
def _process_checkout(request, transaction_id, subscription_plan_id):

    hupler_user = request.user
    transaction = find_transaction(transaction_id)
    new_subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)

    credit_card = transaction.credit_card_details

    cardholder_name = credit_card.cardholder_name
    if cardholder_name is None:
        cardholder_name = ''

    # Transaction records
    payment_details, created = PaymentDetail.objects.get_or_create(
        token=credit_card.token,
        bank_identification_number=credit_card.bin,
        last_4_digits=credit_card.last_4,
        card_type=credit_card.card_type,
        expiration_year=transaction.credit_card['expiration_year'],
        expiration_month=transaction.credit_card['expiration_month'],
        cardholder_name=cardholder_name,
        customer_location=credit_card.customer_location,
    )
    if created:
        payment_details.save()

    transaction_object = Transaction.objects.create(
        user=hupler_user,
        payment_details=payment_details,
        transaction_id=transaction.id,
        transaction_type=transaction.type,
        amount=transaction.amount,
        status=transaction.status,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
    )
    transaction_object.save()

    # Update user subscription plan

    # If user is already subscribed to a plan, delete the old plan and add the new one with extended period
    if UserSubscriptionPlan.objects.filter(user=hupler_user).exists():
        existing_subscription_plan = hupler_user.user_subscription_plan
        old_end_datetime = existing_subscription_plan.subscription_end_datetime

        # delete the old subscription plan
        UserSubscriptionPlan.objects.filter(id=existing_subscription_plan.id).delete()

        # Extend the new subscription plan with leftover days
        extended_end_datetime = old_end_datetime + new_subscription_plan.duration
        new_user_subscription_plan = UserSubscriptionPlan.objects.create(
            user=hupler_user,
            subscription_plan=new_subscription_plan,
            transaction=transaction_object,
            payment_details=payment_details,
        )

        # Send the exnteded date to the save function
        kwargs = {
            'extended_end_datetime': extended_end_datetime,
        }

        new_user_subscription_plan.save(**kwargs)

        return new_user_subscription_plan.id

    # If no subscription plan exists
    else:
        new_user_subscription_plan = UserSubscriptionPlan.objects.create(
            user=hupler_user,
            subscription_plan=new_subscription_plan,
            transaction=transaction_object,
            payment_details=payment_details,
        )
        new_user_subscription_plan.save()

        return new_user_subscription_plan.id


@login_required
def new_checkout(request):
    client_token = generate_client_token()

    if request.method == 'GET':
        subscription_plans = SubscriptionPlan.objects.all()
        context = {
            'client_token': client_token,
            'subscription_plans': subscription_plans,
        }
        return render(request, 'payments/new.html', context=context)

    if request.method == 'POST':

        # Get the selected subscription plan
        subscription_plan_id = request.POST.get('subscription_plan_id')
        subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)

        result = transact({
            'amount': str(subscription_plan.cost_per_transaction),
            'payment_method_nonce': request.POST.get('payment_method_nonce'),
            'options': {
                "submit_for_settlement": True
            }
        })

        # If payment processed successfully, add a subscription plan to the user.
        if result.is_success or result.transaction:

            new_user_subscription_plan_id = _process_checkout(request, result.transaction.id, subscription_plan_id)

            return redirect(
                reverse(
                    'show-checkout',
                    kwargs={
                        'transaction_id': result.transaction.id,
                        'new_user_subscription_plan_id': new_user_subscription_plan_id,
                    },
                )
            )

        else:
            for x in result.errors.deep_errors:
                messages.info(request, x)
            return redirect(reverse('new-checkout'))


@login_required
def show_checkout(request, transaction_id, new_user_subscription_plan_id):

    transaction = find_transaction(transaction_id)
    new_user_subscription_plan = UserSubscriptionPlan.objects.get(id=new_user_subscription_plan_id)

    message = f'Your test transaction of ${transaction.amount} has been successfully processed.'
    message += f'Your current plan is {new_user_subscription_plan.subscription_plan.plan_name}.'
    message += f'Your plan ends on {new_user_subscription_plan.subscription_end_datetime.strftime("%a, %d %B %Y, %I:%M %p")}.'

    if transaction.status in settings.TRANSACTION_SUCCESS_STATUSES:
        context = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': message,
            'transaction': transaction,
        }

    else:
        context = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status,
            'transaction': transaction,
        }

    return render(request, 'payments/show.html', context=context)


class NewTransactionAPIView(generics.GenericAPIView):
    serializer_class = NewTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        client_token = generate_client_token()
        return Response({
            "client_token": client_token,
        }, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        subscription_plan_id = validated_data.get('subscription_plan_id')
        subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
        payment_method_nonce = validated_data.get('payment_method_nonce')

        result = transact({
            'amount': str(subscription_plan.cost_per_transaction),
            'payment_method_nonce': payment_method_nonce,
            'options': {
                "submit_for_settlement": True
            }
        })

        # If payment processed successfully, add a subscription plan to the user.
        if result.is_success or result.transaction:
            transaction_id = result.transaction.id
            transaction = find_transaction(transaction_id)
        else:
            error_messages = []
            for x in result.errors.deep_errors:
                error_messages.append(x)
            return Response({
                "messages": error_messages,
            }, status=status.HTTP_400_BAD_REQUEST)

        if transaction.status in settings.TRANSACTION_SUCCESS_STATUSES:

            new_user_subscription_plan_id = _process_checkout(request, result.transaction.id, subscription_plan_id)

            return Response({
                'new_user_subscription_plan_id': new_user_subscription_plan_id,
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                "message": "Transaction failed",
            }, status=status.HTTP_400_BAD_REQUEST)
