from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import serializers

from djoser.conf import settings

from .models import HuplerUser
from subscriptionplans.utils import check_for_expired_user_subscription_plan


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
    }

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(**params, password=password)
        if not self.user:
            self.user = HuplerUser.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


# Djoser Custom Serializers

# SignUp with custom field
class DjoserSignUpRePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    re_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR,
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR,
    }

    class Meta:
        model = HuplerUser
        fields = [
            'username',
            'email',
            'country',
            'password',
            're_password',
        ]

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")

        user = HuplerUser(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = HuplerUser.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class HuplerUserSerializer(CountryFieldMixin, serializers.ModelSerializer):

    subscription_plan_name = serializers.SerializerMethodField()
    subscription_end_datetime = serializers.SerializerMethodField()
    subscription_plan_id = serializers.SerializerMethodField()

    class Meta:
        model = HuplerUser
        fields = [
            'id',
            'username',
            'email',
            'subscription_plan_name',
            'subscription_end_datetime',
            'subscription_plan_id',
        ]

    def get_subscription_plan_name(self, object):
        check_for_expired_user_subscription_plan(object)
        if hasattr(object, 'user_subscription_plan'):
            return object.user_subscription_plan.subscription_plan.plan_name
        else:
            return None

    def get_subscription_end_datetime(self, object):
        check_for_expired_user_subscription_plan(object)
        if hasattr(object, 'user_subscription_plan'):
            end_datetime = object.user_subscription_plan.subscription_end_datetime
            return end_datetime.strftime("%a, %d %B %Y, %I:%M %p")
        else:
            return None

    def get_subscription_plan_id(self, object):
        check_for_expired_user_subscription_plan(object)
        if hasattr(object, 'user_subscription_plan'):
            return object.user_subscription_plan.subscription_plan.id
        else:
            return None
