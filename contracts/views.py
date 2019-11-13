from django.core.paginator import Paginator

from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from knox.auth import TokenAuthentication

import rest_framework_filters as df_filters

from .models import Contract, Location, Category, Source
from .serializers import ContractSerializer, LocationSerializer, CategorySerializer, SourceSerializer
from subscriptionplans.utils import check_for_expired_user_subscription_plan


# Create your views here.
class ContractsPagination(PageNumberPagination):
    django_paginator_class = Paginator
    page_size = 25


# from https://github.com/carltongibson/django-filter/issues/137
class ContractListFilterSet(df_filters.FilterSet):
    location = df_filters.AllValuesMultipleFilter()
    categories = df_filters.AllValuesMultipleFilter()
    source = df_filters.AllValuesMultipleFilter()

    class Meta:
        model = Contract
        fields = [
            'location',
            'categories',
            'source',
        ]


class ContractList(generics.ListAPIView):

    serializer_class = ContractSerializer
    filterset_class = ContractListFilterSet
    pagination_class = ContractsPagination
    filter_backends = [df_filters.backends.RestFrameworkFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):

        check_for_expired_user_subscription_plan(self.request.user)
        if hasattr(self.request.user, 'user_subscription_plan'):
            return Contract.objects.all().order_by('-rating', '-id')
        else:
            return Contract.objects.filter(
                is_for_free_users=True,
            ).order_by(
                '-rating',
                '-id',
            )


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all().order_by('-id')
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CategoriesList(generics.ListAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class SourceList(generics.ListAPIView):
    queryset = Source.objects.all().order_by('-id')
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
