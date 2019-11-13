from django.contrib import admin

from .models import Category, Location, Skill
from .models import JobDomain, Company, Contract, Source


# Register your models here.

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Skill)
admin.site.register(JobDomain)
admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(Source)
