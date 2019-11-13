from django.urls import path
from . import views

urlpatterns = [
    path('contracts/', views.ContractList.as_view(), name='contracts-list'),
    path('contract_locations/', views.LocationList.as_view(), name='contracts-locations'),
    path('contract_categories/', views.CategoriesList.as_view(), name='contracts-categories'),
    path('contract_sources/', views.SourceList.as_view(), name='contracts-sources')
]
