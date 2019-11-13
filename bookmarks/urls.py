from django.urls import path
from . import views


urlpatterns = [
    path('create_bookmarked_contracts/', views.BookmarkedContractCreate.as_view(), name='create-bookmarked-contracts'),
    path('create_bookmarked_tenders/', views.BookmarkedTenderCreate.as_view(), name='create-bookmarked-tenders'),
    path('bookmarked_contracts/', views.BookmarkedContractList.as_view(), name='bookmarked-contracts'),
    path('bookmarked_tenders/', views.BookmarkedTenderList.as_view(), name='bookmarked-tenders'),
    path('bookmarked_contracts/<int:pk>', views.SingleBookmarkedContract.as_view(), name='single-bookmarked-contract'),
    path('bookmarked_tenders/<int:pk>', views.SingleBookmarkedTender.as_view(), name='single-bookmarked-tender'),
]
