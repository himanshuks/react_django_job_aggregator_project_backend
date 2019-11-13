from django.contrib import admin

from .models import Status, TenderSource, Category, Tender, Location
# Register your models here.

admin.site.register(Status)
admin.site.register(TenderSource)
admin.site.register(Category)
admin.site.register(Tender)
admin.site.register(Location)
