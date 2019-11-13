from django.core.paginator import Paginator

from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from knox.auth import TokenAuthentication

import rest_framework_filters as df_filters

from .models import SocialFeedPost
from .serializers import SocialFeedPostSerializer


# Create your views here.
class SocialFeedPostPagination(PageNumberPagination):
    django_paginator_class = Paginator
    page_size = 10


SOCIAL_FEED_POSTS_CHOICES = (
    (0, 'Twitter'),
    (1, 'Facebook'),
    (2, 'Instagram'),
)


class SocialFeedPostFilterSet(df_filters.FilterSet):
    # is_tweet = df_filters.BooleanFilter()
    # is_facebook_post = df_filters.BooleanFilter()
    # is_instagram_post = df_filters.BooleanFilter()

    social_media_type = df_filters.MultipleChoiceFilter(
        choices=SOCIAL_FEED_POSTS_CHOICES)

    class Meta:
        model = SocialFeedPost
        fields = ['social_media_type']
        # fields = ['is_tweet', 'is_facebook_post', 'is_instagram_post']


class SocialFeedPostList(generics.ListAPIView):

    serializer_class = SocialFeedPostSerializer
    filterset_class = SocialFeedPostFilterSet
    pagination_class = SocialFeedPostPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return SocialFeedPost.objects.all()
