from django.contrib import admin

from .models import Transaction, PaymentDetail

# Register your models here.
admin.site.register(Transaction)
admin.site.register(PaymentDetail)
