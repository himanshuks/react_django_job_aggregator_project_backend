from django.core.management import BaseCommand

from ...models import TwitterUser, Tweet, FacebookPost, SocialFeedPost, InstagramPost


class Command(BaseCommand):

    help = "Clear all Contracts related objects from database"

    def handle(self, *args, **kwargs):
        print("Purging...")
        TwitterUser.objects.all().delete()
        Tweet.objects.all().delete()
        FacebookPost.objects.all().delete()
        InstagramPost.objects.all().delete()
        SocialFeedPost.objects.all().delete()
        print("Done")
