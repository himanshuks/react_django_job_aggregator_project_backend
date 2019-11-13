from rest_framework import serializers

from .models import BookmarkedTender, BookmarkedContract
from contracts.serializers import ContractSerializer
from tenders.serializers import TenderSerializer


class BookmarkedContractListSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookmarkedContract
        fields = ['id', 'contract', 'user', 'is_active']


class BookmarkedTenderListSerializer(serializers.ModelSerializer):
    tender = TenderSerializer()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookmarkedTender
        fields = ['id', 'tender', 'user', 'is_active']


class BookmarkedContractCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookmarkedContract
        fields = ['id', 'contract', 'user', 'is_active']


class BookmarkedTenderCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookmarkedTender
        fields = ['id', 'tender', 'user', 'is_active']
