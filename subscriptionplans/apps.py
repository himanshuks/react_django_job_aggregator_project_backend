from django.apps import AppConfig


class SubscriptionplansConfig(AppConfig):
    name = 'subscriptionplans'

    def ready(self):
        import subscriptionplans.receivers
