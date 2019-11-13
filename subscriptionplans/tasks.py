from django.utils import timezone

from .models import UserSubscriptionPlan

from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name="delete_expired_subscription_plans")
def delete_expired_subscription_plans():
    # Get all the user subcription plans that are expired
    expired_subscription_plans = UserSubscriptionPlan.objects.filter(subscription_end_datetime__lte=timezone.now())
    expired_subscription_plans.delete()
