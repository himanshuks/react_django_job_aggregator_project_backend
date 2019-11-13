from rest_framework import generics
from rest_framework import permissions

from knox.auth import TokenAuthentication

from .models import SubscriptionPlan, UserSubscriptionPlan
from .serializers import SubscriptionPlanSerializer, UserSubscriptionPlanSerializer

# Create your views here.


class SubscriptionPlanList(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class UserSubscriptionPlanList(generics.ListAPIView):

    serializer_class = UserSubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return UserSubscriptionPlan.objects.filter(user=self.request.user)
