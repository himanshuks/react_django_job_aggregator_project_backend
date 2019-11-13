from rest_framework import serializers


class NewTransactionSerializer(serializers.Serializer):

    subscription_plan_id = serializers.IntegerField()
    payment_method_nonce = serializers.CharField()
