import os
import json

from django.core.mail import EmailMultiAlternatives

from .utils import modify_tenders, delete_tenders, populate_tenders_database
from .utils import generate_html_content_new, generate_html_content_amd


def refresh_tenders_database(*args, **kwargs):

    if kwargs['offset']:
        offset = kwargs['offset']
    else:
        offset = 0

    if kwargs['limit']:
        limit = kwargs['limit'] - 1
        limit = limit + offset
    else:
        limit = None

    if kwargs['new']:

        # Read the file
        file = os.path.join('json_data', 'TendersData_PreviousExecution.json')
        with open(file, 'r', encoding='utf-8') as fp:
            json_data = json.load(fp)

        error_data = populate_tenders_database(json_data, offset, limit)
        num_of_failed_data = len(error_data['error'])
        num_of_repeated_data = len(error_data['repeated'])

        subject, from_email, to = 'Tenders Error log', 'from@example.com', 'to@example.com'
        text_content = 'This is an important message.'
        html_content = generate_html_content_new(num_of_failed_data, num_of_repeated_data)
        message = EmailMultiAlternatives(subject, text_content, from_email, [to])
        message.attach_alternative(html_content, "text/html")
        message.attach('populate_tenders_error_data.json', bytes(json.dumps(error_data), encoding='utf-8'))
        message.send()
        return

    # TODO:
    # read from google drive instead of path

    add_error_data = []
    modify_error_data = []
    delete_error_data = []

    # Added Tenders
    added_tenders_file = os.path.join('json_data', 'AddedTenders.json')
    with open(added_tenders_file, 'r', encoding='utf-8') as fp:
        added_tenders_json_data = json.load(fp)

    add_error_data = populate_tenders_database(added_tenders_json_data, offset, limit, add=True)

    # Deleted Tenders
    deleted_tenders_file = os.path.join('json_data', 'RemovedTenders.json')
    with open(deleted_tenders_file, 'r', encoding='utf-8') as fp:
        deleted_tenders_json_data = json.load(fp)

    delete_error_data = delete_tenders(deleted_tenders_json_data, offset, limit)

    # Modified Tenders
    modified_tenders_file = os.path.join('json_data', 'ModifiedTenders.json')
    with open(modified_tenders_file, 'r', encoding='utf-8') as fp:
        modify_tenders_json_data = json.load(fp)

    modify_error_data = modify_tenders(modify_tenders_json_data, offset, limit)

    amd_error_data = {
        'add_error_data': add_error_data,
        'modify_error_data': modify_error_data,
        'delete_error_data': delete_error_data,
    }

    num_of_failed_add_data = len(add_error_data)
    num_of_failed_delete_data = len(delete_error_data)
    num_of_failed_modify_data = len(modify_error_data)

    # Send an email
    subject, from_email, to = 'Add/Modify/Delete Tenders Error log', 'from@example.com', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = generate_html_content_amd(
        num_of_failed_add_data,
        num_of_failed_delete_data,
        num_of_failed_modify_data,
    )
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.attach('amd_tenders_error_data.json', bytes(json.dumps(amd_error_data), encoding='utf-8'))
    message.send()
    return
