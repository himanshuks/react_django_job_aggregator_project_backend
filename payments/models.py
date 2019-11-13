from django.db import models

from hupleruser.models import HuplerUser


# Create your models here.
class PaymentDetail(models.Model):

    token = models.CharField(max_length=100, null=True, blank=True)  # Can be some other field? (future)
    bank_identification_number = models.IntegerField(unique=True)
    last_4_digits = models.IntegerField()
    card_type = models.CharField(max_length=100)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cardholder_name = models.CharField(max_length=200, blank=True)
    customer_location = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.last_4_digits} | {self.card_type}"


class Transaction(models.Model):

    user = models.ForeignKey(HuplerUser, related_name='transactions', on_delete=models.CASCADE)
    payment_details = models.ForeignKey(
        PaymentDetail,
        related_name='transactions',
        null=True,
        on_delete=models.SET_NULL)

    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_type = models.CharField(max_length=50)
    amount = models.FloatField()
    status = models.CharField(max_length=50)  # Can be a FK to a model. There are finite choices for this
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_id}"
