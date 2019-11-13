from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.dispatch import receiver

# from rest_framework.authtoken.models import Token

from knox.models import AuthToken

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        AuthToken.objects.create(user=instance)


class HuplerUser(AbstractUser):
    country = CountryField(blank_label='Select Country')
    email = models.EmailField(unique=True)
