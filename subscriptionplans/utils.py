from django.utils import timezone

from .models import UserSubscriptionPlan


def check_for_expired_user_subscription_plan(user):
    try:
        UserSubscriptionPlan.objects.get(user=user)
        user_subscription_plan = UserSubscriptionPlan.objects.filter(
            user=user,
            subscription_end_datetime__lte=timezone.now()
        )
        if user_subscription_plan:
            # print("Deleting -- ", user_subscription_plan)
            user_subscription_plan.delete()

    except UserSubscriptionPlan.DoesNotExist:
        pass
    except UserSubscriptionPlan.MultipleObjectsReturned:
        # print("MULTIPLE USER SUBSCRIPTION PLANS FOUND")
        user_subscription_plans = UserSubscriptionPlan.objects.filter(user=user)
        user_subscription_plans.delete()
