from django.urls import path
from . import views

urlpatterns = [
    path('subscription_plans/', views.SubscriptionPlanList.as_view(), name='subscription-plans-list'),
    path('user_subscription_plans/', views.UserSubscriptionPlanList.as_view(), name='user-subscription-plans'),
]
