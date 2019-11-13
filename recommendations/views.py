from django.utils import timezone

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from knox.auth import TokenAuthentication

from .models import RecommendedContracts, RecommendedTenders

from contracts.views import ContractListFilterSet, ContractsPagination
from contracts.serializers import ContractSerializer

from tenders.views import TenderListFilterSet, TenderPagination
from tenders.serializers import TenderSerializer

from subscriptionplans.utils import check_for_expired_user_subscription_plan


# Create your views here.
class RecommendedContractsList(generics.ListAPIView):

    serializer_class = ContractSerializer
    filterset_class = ContractListFilterSet
    pagination_class = ContractsPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        check_for_expired_user_subscription_plan(object)
        if hasattr(self.request.user, 'user_subscription_plan'):
            return super().get(request, *args, **kwargs)
        raise PermissionDenied("User has not subscribed")

    def get_queryset(self):
        return RecommendedContracts.objects.get(user=self.request.user).contracts.all()


class RecommendedTendersList(generics.ListAPIView):

    serializer_class = TenderSerializer
    filterset_class = TenderListFilterSet
    pagination_class = TenderPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        check_for_expired_user_subscription_plan(object)
        if hasattr(self.request.user, 'user_subscription_plan'):
            return super().get(request, *args, **kwargs)
        raise PermissionDenied("User has not subscribed")

    def get_queryset(self):
        return RecommendedTenders.objects.get(user=self.request.user).tenders.all()
