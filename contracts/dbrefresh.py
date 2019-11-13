import os
import json

from django.core.mail import EmailMultiAlternatives

from .utils import modify_contracts, delete_contracts, populate_contracts_database
from .utils import generate_html_content_new, generate_html_content_amd


def refresh_contracts_database(*args, **kwargs):

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

        file = os.path.join('json_data', 'JobsData_PreviousExecution.json')
        with open(file, 'r', encoding='utf-8') as fp:
            json_data = json.load(fp)

        error_data = populate_contracts_database(json_data, offset, limit)
        num_of_failed_data = len(error_data['error'])
        num_of_repeated_data = len(error_data['repeated'])

        subject, from_email, to = 'Contracts Error log', 'from@example.com', 'to@example.com'
        text_content = 'This is an important message.'
        html_content = generate_html_content_new(num_of_failed_data, num_of_repeated_data)
        message = EmailMultiAlternatives(subject, text_content, from_email, [to])
        message.attach_alternative(html_content, "text/html")
        message.attach('populate_contracts_error_data.json', bytes(json.dumps(error_data), encoding='utf-8'))
        message.send()
        return

    # TODO:
    # read from google drive instead of path

    add_error_data = []
    modify_error_data = []
    delete_error_data = []

    # Added Contracts
    added_contracts_file = os.path.join('json_data', 'AddedJobs.json')
    with open(added_contracts_file, 'r', encoding='utf-8') as fp:
        added_contracts_json_data = json.load(fp)

    add_error_data = populate_contracts_database(added_contracts_json_data, offset, limit, add=True)

    # Deleted Contracts
    deleted_contracts_file = os.path.join('json_data', 'RemovedJobs.json')
    with open(deleted_contracts_file, 'r', encoding='utf-8') as fp:
        deleted_contracts_json_data = json.load(fp)

    delete_error_data = delete_contracts(deleted_contracts_json_data, offset, limit)

    # Modified Contracts
    modified_contracts_file = os.path.join('json_data', 'ModifiedJobs.json')
    with open(modified_contracts_file, 'r', encoding='utf-8') as fp:
        modify_contracts_json_data = json.load(fp)

    modify_error_data = modify_contracts(modify_contracts_json_data, offset, limit)

    amd_error_data = {
        'add_error_data': add_error_data,
        'modify_error_data': modify_error_data,
        'delete_error_data': delete_error_data,
    }

    num_of_failed_add_data = len(add_error_data)
    num_of_failed_delete_data = len(delete_error_data)
    num_of_failed_modify_data = len(modify_error_data)

    # Send an email
    subject, from_email, to = 'Add/Modify/Delete Contracts Error log', 'from@example.com', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = generate_html_content_amd(
        num_of_failed_add_data,
        num_of_failed_delete_data,
        num_of_failed_modify_data,
    )
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.attach('amd_contracts_error_data.json', bytes(json.dumps(amd_error_data), encoding='utf-8'))
    message.send()
    return
