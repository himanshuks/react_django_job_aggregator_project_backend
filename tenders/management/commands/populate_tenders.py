from django.core.management import BaseCommand

from ...dbrefresh import refresh_tenders_database


class Command(BaseCommand):

    help = "Populate Database using json_data/TendersData_PreviousExecution.json file or the new 3-file system"

    def add_arguments(self, parser):

        # Optional argument
        parser.add_argument('-n', '--new', type=bool, help='Populate for the first time?')
        parser.add_argument('-l', '--limit', type=int, help='Define a limit for number of records to be entered')
        parser.add_argument('-o', '--offset', type=int, help='Define an offset to start the iteration at')

    def handle(self, *args, **kwargs):
        refresh_tenders_database(*args, **kwargs)