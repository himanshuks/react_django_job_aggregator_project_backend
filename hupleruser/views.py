from django.utils import timezone
from django.contrib.auth import user_logged_in

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField

from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.settings import knox_settings

from django_countries import countries

from .models import HuplerUser
from .serializers import HuplerUserSerializer, LoginSerializer


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def get_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def post(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)

        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)


class CountryListAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        countries_dict = dict(countries)
        return Response(countries_dict, status=status.HTTP_200_OK)


class HuplerUserProfile(generics.ListAPIView):
    serializer_class = HuplerUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return HuplerUser.objects.filter(id=self.request.user.id)
