from django.core.management import BaseCommand

from ...models import Contract, Company, Location, Skill, Category, JobDomain, Source


class Command(BaseCommand):

    help = "Clear all Contracts related objects from database"

    def handle(self, *args, **kwargs):
        print("Purging...")
        Contract.objects.all().delete()
        Company.objects.all().delete()
        Location.objects.all().delete()
        Skill.objects.all().delete()
        Category.objects.all().delete()
        JobDomain.objects.all().delete()
        Source.objects.all().delete()
        print("Done")
