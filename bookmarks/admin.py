from django.contrib import admin

from .models import BookmarkedContract, BookmarkedTender

# Register your models here.
admin.site.register(BookmarkedTender)
admin.site.register(BookmarkedContract)
