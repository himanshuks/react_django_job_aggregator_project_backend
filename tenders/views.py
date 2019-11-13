from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from knox.auth import TokenAuthentication

import rest_framework_filters as df_filters

from .models import Tender, TenderSource, Location
from .serializers import TenderSerializer, LocationSerializer

from subscriptionplans.utils import check_for_expired_user_subscription_plan


class TenderPagination(PageNumberPagination):
    django_paginator_class = Paginator
    page_size = 10


class TenderListFilterSet(df_filters.FilterSet):
    location = df_filters.AllValuesMultipleFilter()
    source = df_filters.ModelChoiceFilter(queryset=TenderSource.objects.all())

    class Meta:
        model = Tender
        fields = ['location', 'source']


class TenderList(generics.ListAPIView):

    serializer_class = TenderSerializer
    filterset_class = TenderListFilterSet
    pagination_class = TenderPagination
    filter_backends = [df_filters.backends.RestFrameworkFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        check_for_expired_user_subscription_plan(self.request.user)
        if hasattr(self.request.user, 'user_subscription_plan'):
            return Tender.objects.all().order_by('-rating', '-id')
        else:
            return Tender.objects.filter(
                is_for_free_users=True,
            ).order_by(
                '-rating',
                '-id',
            )


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
