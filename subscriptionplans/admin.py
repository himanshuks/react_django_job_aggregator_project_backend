from django.contrib import admin
from .models import SubscriptionPlan, UserSubscriptionPlan
# Register your models here.

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscriptionPlan)
