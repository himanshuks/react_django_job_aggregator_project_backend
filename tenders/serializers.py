from rest_framework import serializers
from .models import Status, TenderSource, Category, Tender, Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'location_name']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['id', 'tender_status']


class TenderSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenderSource
        fields = ['id', 'tender_source']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'tender_category_name']


class TenderSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    source = TenderSourceSerializer()
    status = StatusSerializer()
    location = LocationSerializer()

    class Meta:
        model = Tender
        fields = [
            'id',
            'title',
            'value',
            'url',
            'closing_datetime',
            'published_datetime',
            'category',
            'source',
            'status',
            'location',
        ]
