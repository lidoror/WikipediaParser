import string
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString


# I needed to find a way to get  the page content in order to parse and filter it to get the data
def get_page_date(url: str) -> str:
    """
    this function send get request to url and return the response in string format
    :param url: the website url we send the request to
    :return: string format of the url response
    """
    return requests.get(url).text


# I needed a way to work with the html data we got from the site the second option after panda was beautiful soup
def parse_html_website(html: str) -> BeautifulSoup:
    """
    this function parse the html string to BeautifulSoup object
    :param html: the string we got from the website
    :return: beautifulsoup object that is the parsed string
    """
    return BeautifulSoup(html, 'html.parser')


# I started in trying to get the headers of the table and then the data, but I found a better way to do it
def find_headers(table) -> list:
    """
    this function find the headers of the table
    :param table: the table we want to find the headers in
    :return: list of the headers in the table
    """
    # I created a list comprehension that will return the headers of the table
    return [headers for headers in table.find('tr').text.splitlines() if headers]


# i was able to the names in the table easily, but I had a problem getting the collateral_adjective in this way
def get_animal_names(table) -> list:
    """
    this function get the table and return the names of the animals in the table
    :param table: the table we want to get the names from
    :return: list of the names of the animals in the table
    """
    # because this way returned the letter headers which separate the tables to i created a list of the letters and
    # made sure that if the letters are in the data we won't insert it
    letters = [f'{letter}\n' for letter in string.ascii_uppercase]
    rows = table.findChildren('tr')
    # I created a list comprehension that will return the names of the animals in the table
    # I did it after finding out in debug mode where the data I needed was located in the object
    return [name.contents[1].text for name in rows if name.contents[1].text not in letters]


# in the end that was the best way I found to get the data I needed this way I was able to get the data in one run
# and made sure the data of the name is with the right collateral adjective
def get_data_json_format(table) -> dict:
    """
    this function get the table and return the data in json format
    :param table: the table we want to get the data from
    :return: json format of the data in the table the key is the animal name and the value is the collateral adjective
    """
    data = {}
    # i created a list of the letters and made sure that if the letters are in the data we won't insert it
    letters = [f'{letter}\n' for letter in string.ascii_uppercase]

    rows = table.findChildren('tr')
    # we loop over the rows and get the name of the animal and the collateral adjective
    for row in rows:
        # I added this if statement to make sure that the letters won't be inserted in the data because when we get
        # to the letter (which we don't need anyway in the data) we get an exception because we try to access a data
        # that doesn't exist
        if row.contents[1].text in letters or row.contents[1].text == 'Animal':
            continue
        # in debug mode I found out that the name is in the filed named contents and this is the second value also we
        # used the text field to make sure we get the text and not the html tags
        animal_name = row.contents[1].text
        # after some time in debug mode and research I found out that the collateral adjective is in the 11th filed
        # and teh right data belong to object named NavigableString, so I made sure that only this data added to the
        # dictionary
        collateral_adjective = [str(i.text) for i in row.contents[11].contents if isinstance(i, NavigableString)]
        # I put the data in variables because I think its more readable this way
        # it's easier to read name than reading data in certain place
        data[animal_name] = collateral_adjective

    return data
