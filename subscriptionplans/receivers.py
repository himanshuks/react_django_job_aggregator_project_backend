from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from .utils import check_for_expired_user_subscription_plan


@receiver(user_logged_in)
def check_for_expired_user_subscription_plan_receiver(sender, user, request, **kwargs):
    check_for_expired_user_subscription_plan(user)
