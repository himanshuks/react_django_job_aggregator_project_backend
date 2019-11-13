import os
import json
import pytz
from datetime import datetime

from .models import Tender, Location, TenderSource

DATETIME_STRING_FORMAT = '%Y-%m-%d %H:%M:%S'


def generate_html_content_amd(num_of_failed_add_data, num_of_failed_delete_data, num_of_failed_modify_data):
    html_string = f"""\
<h1> Add/Modify/Delete Tenders Error Report </h1>
<h2> Add Tenders </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_add_data}"</p>
<br>
<h2> Delete Tenders </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_delete_data}"</p>
<br>
<h2> Modify Tenders </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_modify_data}"</p>
"""

    return html_string


def generate_html_content_new(num_of_failed_data, num_of_repeated_data):
    html_string = f"""\
<h1> Tenders Error Report </h1>
<p> Total number of records that were erroneous = {num_of_failed_data}")</p>
<p> Total number of repeated records = {num_of_repeated_data}")</p>
"""

    return html_string


def populate_tenders_database(json_data, offset=0, limit=None, add=False):

    iteration = 0
    failed_data = []
    repeat_count = 0
    repeated_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            if entry['TenderLocation'] is not None:
                location, created = Location.objects.get_or_create(
                    location_name=entry['TenderLocation'],
                )
            else:
                location = None

            if entry['PublishedVia'] is not None:
                tender_source, created = TenderSource.objects.get_or_create(
                    tender_source=entry['PublishedVia'],
                )
            else:
                tender_source = None

            closing_datetime = datetime.strptime(
                entry['TenderClosingDate'],
                DATETIME_STRING_FORMAT).replace(tzinfo=pytz.utc)

            tender, created = Tender.objects.get_or_create(
                title=entry['TenderTitle'],
                url=entry['TenderUrl'],
                is_for_free_users=entry['isForFreeUsers'],
                closing_datetime=closing_datetime,
                source=tender_source,
                location=location,
            )

            if created:
                print(f"Iteration {iteration} - successful.")
            else:
                repeat_count += 1
                repeated_data.append((entry, iteration))
                raise Exception("Repeated entry")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")
    print(f"total number of repeated records = {repeat_count}")

    error_data = {
        'repeated': repeated_data,
        'error': failed_data,
    }

    # error log
    if add:
        error_file = os.path.join('json_data', 'temp', 'add_tenders_error_data.json')
    else:
        error_file = os.path.join('json_data', 'temp', 'populate_tenders_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(error_data, fp, indent=4)

    return error_data


def delete_tenders(json_data, offset=0, limit=None):

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            if entry['TenderLocation'] is not None:
                location = Location.objects.get(
                    location_name=entry['TenderLocation'],
                )
            else:
                location = None

            if entry['PublishedVia'] is not None:
                tender_source = TenderSource.objects.get(
                    tender_source=entry['PublishedVia'],
                )
            else:
                tender_source = None

            try:
                closing_datetime = datetime.strptime(
                    entry['TenderClosingDate'],
                    DATETIME_STRING_FORMAT).replace(tzinfo=pytz.utc)

                tender = Tender.objects.get(
                    title=entry['TenderTitle'],
                    url=entry['TenderUrl'],
                    is_for_free_users=entry['isForFreeUsers'],
                    closing_datetime=closing_datetime,
                    source=tender_source,
                    location=location,
                )

                tender.delete()
                print(f"Iteration {iteration} - successful.")

            except Tender.DoesNotExist as e:
                raise Exception("Tender does not exist", str(e))

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))

            # TODO:
            # Change prints to log
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_file = os.path.join('json_data', 'temp', 'delete_tenders_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)

    return failed_data


def modify_tenders(json_data, offset=0, limit=None):

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            try:
                tender = Tender.objects.get(
                    url=entry['TenderUrl'],
                )

            except Tender.DoesNotExist as e:
                raise Exception("Tender does not exist", str(e))

            if entry['TenderLocation'] is not None:
                location, created = Location.objects.get_or_create(
                    location_name=entry['TenderLocation'],
                )
            else:
                location = None

            if entry['PublishedVia'] is not None:
                tender_source, created = TenderSource.objects.get_or_create(
                    tender_source=entry['PublishedVia'],
                )
            else:
                tender_source = None

            closing_datetime = datetime.strptime(
                entry['TenderClosingDate'],
                DATETIME_STRING_FORMAT).replace(tzinfo=pytz.utc)

            tender.title = entry['TenderTitle']
            tender.is_for_free_users = entry['isForFreeUsers']
            tender.closing_datetime = closing_datetime
            tender.source = tender_source
            tender.location = location

            tender.save()

            print(f"Iteration {iteration} - successful.")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))

            # TODO:
            # Change prints to log
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_file = os.path.join('json_data', 'temp', 'modify_tenders_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)

    return failed_data
