from django.urls import path, re_path
from . import views


urlpatterns = [
    path('new/', views.new_checkout, name='new-checkout'),
    re_path('show_transaction/(?P<transaction_id>.*)/(?P<new_user_subscription_plan_id>[0-9]*)/', views.show_checkout, name='show-checkout'),

    path('checkout/new/', views.NewTransactionAPIView.as_view(), name='new-transaction-api'),
]
