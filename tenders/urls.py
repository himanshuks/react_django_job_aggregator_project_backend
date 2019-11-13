from django.urls import path
from . import views

urlpatterns = [
    path('tenders/', views.TenderList.as_view(), name='tenders_list'),
    path('tender_locations/', views.LocationList.as_view(), name='tenders_locations'),
]
