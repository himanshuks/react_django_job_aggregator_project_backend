from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import HuplerUser


# Register your models here.
class HuplerUserAdmin(UserAdmin):
    model = HuplerUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


admin.site.register(HuplerUser, HuplerUserAdmin)
