from django.utils import timezone
from django.db import models

from hupleruser.models import HuplerUser
from payments.models import PaymentDetail, Transaction


# Create your models here.
class SubscriptionPlan(models.Model):

    plan_name = models.CharField(max_length=100, unique=True)
    cost_per_transaction = models.FloatField()
    duration = models.DurationField()

    def __str__(self):
        return self.plan_name.title()


class UserSubscriptionPlan(models.Model):

    user = models.OneToOneField(
        HuplerUser,
        related_name='user_subscription_plan',
        on_delete=models.CASCADE,
    )
    transaction = models.OneToOneField(
        Transaction,
        related_name='user_subscription_plan',
        on_delete=models.DO_NOTHING,
    )
    payment_details = models.ForeignKey(
        PaymentDetail,
        related_name='user_subscription_plan',
        on_delete=models.DO_NOTHING,
    )

    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        related_name='user_subscription_plan',
        on_delete=models.CASCADE
    )

    subscription_start_datetime = models.DateTimeField(auto_now_add=True)
    subscription_end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} | {self.subscription_plan.plan_name} | {self.transaction.transaction_id}"

    def save(self, *args, **kwargs):
        # If subscription is being extended
        if 'extended_end_datetime' in kwargs:
            self.subscription_end_datetime = kwargs.pop('extended_end_datetime')
        else:
            if not self.subscription_start_datetime:
                self.subscription_start_datetime = timezone.now()
            self.subscription_end_datetime = self.subscription_start_datetime + self.subscription_plan.duration
        super().save(*args, **kwargs)
