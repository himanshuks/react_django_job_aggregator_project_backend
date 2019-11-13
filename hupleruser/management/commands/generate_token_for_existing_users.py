from django.core.management import BaseCommand

from knox.models import AuthToken

from ...models import HuplerUser


class Command(BaseCommand):

    help = "Generate token for existing users"

    def handle(self, *args, **kwargs):

        users = HuplerUser.objects.all()

        for user in users:
            try:
                token = AuthToken.objects.get(user=user)
                print(user.username, token)
            except AuthToken.DoesNotExist:
                token_instance, token = AuthToken.objects.create(user=user)
                print(user.username, token)
            except AuthToken.MultipleObjectsReturned:
                token = AuthToken.objects.filter(user=user).first()
                print(user.username, token)
