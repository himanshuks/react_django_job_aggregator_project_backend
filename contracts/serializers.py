from django.utils.text import Truncator

from rest_framework import serializers

from .models import Category, Company, Contract, JobDomain, Location, Skill, Source


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_name']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name']


class JobDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDomain
        fields = ['id', 'domain_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'company_logo_url']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'source_name', 'source_logo_url']


class ContractSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    location = LocationSerializer()
    source = SourceSerializer()
    skills = SkillSerializer(many=True)
    domains = JobDomainSerializer(many=True)
    categories = CategorySerializer(many=True)
    truncated_description = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'id',
            'title',
            'posted_datetime',
            'salary',
            'description',
            'url',
            'company',
            'location',
            'categories',
            'source',
            'skills',
            'domains',
            'truncated_description',
        ]

    def get_truncated_description(self, object):
        full_description = object.description
        return Truncator(full_description).words(100)
