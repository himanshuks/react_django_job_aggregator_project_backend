from rest_framework import serializers

from .models import SubscriptionPlan, UserSubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'plan_name', 'cost_per_transaction', 'duration']


class UserSubscriptionPlanSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = UserSubscriptionPlan
        fields = [
            'user',
            'transaction',
            'payment_details',
            'subscription_plan',
            'subscription_start_datetime',
            'subscription_end_datetime',
        ]
