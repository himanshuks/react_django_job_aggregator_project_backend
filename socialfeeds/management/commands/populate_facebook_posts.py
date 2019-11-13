from django.core.management import BaseCommand

from ...dbrefresh import populate_facebook_posts


class Command(BaseCommand):

    help = "Populate Database using json_data/Facebook.json file"

    def add_arguments(self, parser):

        # Optional argument
        parser.add_argument('-l', '--limit', type=int, help='Define a limit for number of records to be entered')
        parser.add_argument('-o', '--offset', type=int, help='Define an offset to start the iteration at')

    def handle(self, *args, **kwargs):
        populate_facebook_posts(*args, **kwargs)
