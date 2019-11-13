from django.core.management import BaseCommand

from ...models import Location, Status, TenderSource, Category, Tender


class Command(BaseCommand):

    help = "Clear all Tenders related objects from database"

    def handle(self, *args, **kwargs):
        print("Purging...")
        Location.objects.all().delete()
        Status.objects.all().delete()
        TenderSource.objects.all().delete()
        Category.objects.all().delete()
        Tender.objects.all().delete()
        print("Done")
