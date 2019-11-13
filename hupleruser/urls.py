from django.urls import path
from django.urls import include

from knox import views as knox_views

from . import views


urlpatterns = [
    # djoser
    path(r'auth/', include('djoser.urls')),

    # hupler/knox
    path('auth/token/login/', views.LoginAPIView.as_view(), name='hupler-login'),
    path('auth/token/logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('auth/token/logout_all/', knox_views.LogoutAllView.as_view(), name='knox-logoutall'),

    # custom api for signup form
    path('countries/', views.CountryListAPIView.as_view(), name='countries-list'),
]
