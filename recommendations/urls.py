from django.urls import path
from . import views

urlpatterns = [
    path('recommended_contracts/', views.RecommendedContractsList.as_view(), name='recommended-contracts'),
    path('recommended_tenders/', views.RecommendedTendersList.as_view(), name='recommended-tenders'),
]
