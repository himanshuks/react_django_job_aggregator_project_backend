import os
import json

from .models import Contract, Company, Location, Skill, Category, Source


def generate_html_content_amd(num_of_failed_add_data, num_of_failed_delete_data, num_of_failed_modify_data):
    html_string = f"""\
<h1> Add/Modify/Delete Contracts Error Report </h1>
<h2> Add Contracts </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_add_data}"</p>
<br>
<h2> Delete Contracts </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_delete_data}"</p>
<br>
<h2> Modify Contracts </h2>
<hr>
<p> Total number of records that were erroneous = {num_of_failed_modify_data}"</p>
"""

    return html_string


def generate_html_content_new(num_of_failed_data, num_of_repeated_data):
    html_string = f"""\
<h1> Contracts Error Report </h1>
<p> Total number of records that were erroneous = {num_of_failed_data}"</p>
<p> Total number of repeated records = {num_of_repeated_data}"</p>
"""

    return html_string


def populate_contracts_database(json_data, offset=0, limit=None, add=False):

    iteration = 0
    failed_data = []
    repeat_count = 0
    repeated_data = []

    for entry in json_data[offset:limit]:
        iteration += 1
        skills = []
        categories = []

        try:

            if entry['JobCompanyName'] is not None:
                company, created = Company.objects.get_or_create(
                    company_name=entry['JobCompanyName'],
                    # company_logo_url=None,  # See if this takes default
                )
            else:
                company = None

            if entry['JobLocation'] is not None:
                location, created = Location.objects.get_or_create(
                    location_name=entry['JobLocation'],
                )
            else:
                location = None

            if entry['JobSkills'] is not None:
                skill_names = entry['JobSkills'].split(' , ')
                for skill_name in skill_names:
                    skill, created = Skill.objects.get_or_create(
                        skill_name=skill_name,
                    )
                skills.append(skill)
            else:
                skills = None

            # Mandatory fields
            category_names = entry['JobCategory'].split(' , ')
            for category_name in category_names:
                category, created = Category.objects.get_or_create(
                    category_name=category_name,
                )
            categories.append(category)

            source, created = Source.objects.get_or_create(
                source_name=entry['JobSource'],
                source_logo_url=entry['LogoUrl'],
            )

            contract, created = Contract.objects.get_or_create(
                title=entry['JobTitle'],
                salary=entry['JobSalary'],
                description=entry['JobDescription'],
                rating=entry['DisplayOrderRating'],
                url=entry['JobUrl'],
                is_for_free_users=entry['isForFreeUsers'],
                company=company,
                location=location,
                source=source,
            )

            if created:
                if skills is not None:
                    contract.skills.set(skills)
                contract.categories.set(categories)
                contract.save()
                print(f"Iteration {iteration} - successful.")
            else:
                repeat_count += 1
                repeated_data.append((entry, iteration))
                raise Exception("Repeated entry")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")
    print(f"total number of repeated records = {len(repeated_data)}")

    error_data = {
        'repeated': repeated_data,
        'error': failed_data,
    }

    # error log
    if add:
        error_file = os.path.join('json_data', 'temp', 'add_contracts_error_data.json')
    else:
        error_file = os.path.join('json_data', 'temp', 'populate_contracts_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(error_data, fp, indent=4)

    return error_data


def delete_contracts(json_data, offset=0, limit=None):

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            if entry['JobCompanyName'] is not None:
                company = Company.objects.get(
                    company_name=entry['JobCompanyName'],
                    # company_logo_url=None,  # See if this takes default
                )
            else:
                company = None

            if entry['JobLocation'] is not None:
                location = Location.objects.get(
                    location_name=entry['JobLocation'],
                )
            else:
                location = None

            source = Source.objects.get(
                source_name=entry['JobSource'],
                source_logo_url=entry['LogoUrl'],
            )

            try:
                contract = Contract.objects.get(
                    title=entry['JobTitle'],
                    salary=entry['JobSalary'],
                    description=entry['JobDescription'],
                    url=entry['JobUrl'],
                    rating=entry['DisplayOrderRating'],
                    is_for_free_users=entry['isForFreeUsers'],
                    company=company,
                    location=location,
                    source=source,
                )

                contract.delete()
                print(f"Iteration {iteration} - successful.")

            except Contract.DoesNotExist as e:
                raise Exception("Contract does not exist, ", str(e))

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))

            # TODO:
            # Change prints to log
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_file = os.path.join('json_data', 'temp', 'delete_contracts_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)

    return failed_data


def modify_contracts(json_data, offset=0, limit=None):

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1
        skills = []
        categories = []

        try:

            try:
                contract = Contract.objects.get(
                    url=entry['JobUrl'],
                )

            except Contract.DoesNotExist as e:
                raise Exception("Contract does not exist", str(e))

            if entry['JobCompanyName'] is not None:
                company, created = Company.objects.get_or_create(
                    company_name=entry['JobCompanyName'],
                    # company_logo_url=None,  # See if this takes default
                )
            else:
                company = None

            if entry['JobLocation'] is not None:
                location, created = Location.objects.get_or_create(
                    location_name=entry['JobLocation'],
                )
            else:
                location = None

            if entry['JobSkills'] is not None:
                skill_names = entry['JobSkills'].split(' , ')
                for skill_name in skill_names:
                    skill, created = Skill.objects.get_or_create(
                        skill_name=skill_name,
                    )
                skills.append(skill)
            else:
                skills = None

            # Mandatory fields
            category_names = entry['JobCategory'].split(' , ')
            for category_name in category_names:
                category, created = Category.objects.get_or_create(
                    category_name=category_name,
                )
            categories.append(category)

            source = Source.objects.get(
                source_name=entry['JobSource'],
                source_logo_url=entry['LogoUrl'],
            )

            contract.title = entry['JobTitle']
            contract.salary = entry['JobSalary']
            contract.description = entry['JobDescription']
            contract.rating = entry['DisplayOrderRating']
            contract.is_for_free_users = entry['isForFreeUsers']
            contract.company = company
            contract.location = location
            contract.source = source
            contract.categories.set(categories)

            if skills is not None:
                contract.skills.set(skills)

            contract.save()

            print(f"Iteration {iteration} - successful.")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))

            # TODO:
            # Change prints to log
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_file = os.path.join('json_data', 'temp', 'modify_contracts_error_data.json')
    with open(error_file, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)

    return failed_data
