import json
import requests.exceptions
import utils
import os.path

try:
    url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
    page_content = utils.get_page_date(url)

    parsed_website = utils.parse_html_website(page_content)

    table_to_filter = parsed_website.findAll('table')[-1]

    page_data = utils.get_data_json_format(table_to_filter).items()

    # because we save the data in the txt file in append mode we need to make sure that the file is empty so the data
    # won't be duplicated
    if os.path.exists('./animals.txt'):
        os.remove('./animals.txt')

    # we loop throw the dictionary and print the animal name and the collateral adjective in prettier way
    for animal, collateral_adjective in page_data:
        collateral_adjective = ' '.join(collateral_adjective)
        print(f'animal: {animal} , collateral adjective: {collateral_adjective}')

        # in this way we create txt file and write the data in it
        with open('animals.txt', 'a') as file:
            file.write(f'animal: {animal} , collateral adjective: {collateral_adjective}\n')

    # in this way we create json file and write the data in it with indent of 4 spaces which make it more readable
    with open('animals.json', 'w') as file:
        file.write(json.dumps(dict(page_data), indent=4))

# this will catch exception if the url is not valid
except requests.exceptions.MissingSchema as url_error:
    print('sorry we could not find the url you entered')
# this will catch exception if the table is not found
except IndexError as index_error:
    print('sorry we could not find the table you are looking for')
# this will catch all teh rest exceptions we put it in order to prevent unhanded exceptions in our program that could
# make our progream crash
except Exception as error:
    print('some problem occurred please try again later')
