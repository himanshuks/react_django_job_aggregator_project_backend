from django.contrib import admin

from .models import RecommendedContracts, RecommendedTenders


# Register your models here.
admin.site.register(RecommendedContracts)
admin.site.register(RecommendedTenders)
