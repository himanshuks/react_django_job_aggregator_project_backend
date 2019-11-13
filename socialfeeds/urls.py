from django.urls import path
from . import views

urlpatterns = [
    path('social_feed_posts/', views.SocialFeedPostList.as_view(), name='socialfeed-posts-list'),
]
