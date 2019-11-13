from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.fields import CountryField

from .models import HuplerUser


class CustomUserCreationForm(UserCreationForm):
    country = CountryField(blank_label='(select country)')

    class Meta(UserCreationForm):
        model = HuplerUser
        fields = ('username', 'email', 'country')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = HuplerUser
        fields = UserChangeForm.Meta.fields
