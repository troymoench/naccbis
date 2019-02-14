""" This module provides general scraping functions as well as
some utility functions used in the scraping process.
"""
# Standard library imports
import logging
import sys
from time import sleep
# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
# Local imports


# ********************************
# ** General Scraping Functions **
# ********************************
def get_soup(url, backoff=1, verbose=False):
    """ Create a BeautifulSoup object from a web page with the requested URL

    :param url: A string with the requested URL
    :param backoff: Number of seconds to sleep to prevent overloading the server
    :param verbose: Print extra information to standard out?
    :returns: A BeautifulSoup object
    """
    logging.debug("Backing off for %f seconds", backoff)
    sleep(backoff)  # to prevent overloading the server
    if verbose:
        print("GET " + url)
    try:
        request = requests.get(url, timeout=15)
    except requests.exceptions.RequestException:
        print("Error: Unable to connect to", url)
        logging.critical("Error: Unable to connect to", url)
        sys.exit(1)
    else:
        text = request.text
        return BeautifulSoup(text, "html.parser")


def get_text(html_tag):
    """ Get the inner HTML from a BeautifulSoup tag and strip whitespace.

    :param html_tag: BeautifulSoup tag
    :returns: The inner HTML as a string
    """
    return html_tag.text.strip()


def get_href(html_tag):
    """ Get the href attribute from a BeautifulSoup tag

    :param html_tag: BeautifulSoup tag
    :returns: The href attribute as a string
    """
    return html_tag.attrs['href']


def find_table(soup_obj, header_values, verbose=False):
    """ Find HTML tables that contain the specified header values.
    Note that header value matching is case insensitive.

    :param soup_obj: BeautifulSoup object to search
    :param header_values: A list of header values to search for
    :param verbose: Print extra information to standard out?
    :returns: A list of table indices. Returns an empty list if table not found.
    """
    header_values = [x.lower() for x in header_values]

    indices = []
    tables = soup_obj.find_all('table')
    for i, table in enumerate(tables):
        header = table.find_all('th')
        columns = [x.text.strip().lower() for x in header]
        if set(header_values).issubset(set(columns)):
            indices.append(i)
        else:
            if verbose:  # this needs some work
                print("Missing values in table {}: {}".format(i, set(header_values) - set(columns)))
    logging.debug("Found %d tables with matching headers", len(indices))
    return indices


def scrape_table(soup, tbl_num, first_row=2, skip_rows=0):
    """ Scrape HTML table with the specified index and populate a DataFrame.

    :param soup: BeautifulSoup object containing the table
    :param tbl_num: Integer index that specifies the table to scrape. Note that
                    the index is 1 based.
    :param first_row: First table row that will populate the DataFrame
    :param skip_rows: Number of rows to skip on the bottom of the table
    :returns: A DataFrame of the raw scraped table
    """
    table = soup.find_all('table')[tbl_num - 1]
    html_th = table.find_all('th')
    headers = [x.text.strip() for x in html_th]

    html_rows = table.find_all('tr')
    rows = html_rows[first_row - 1:len(html_rows) - skip_rows]
    logging.debug("Found %d table rows", len(rows))

    # Empty DataFrame to add rows to
    df = pd.DataFrame(columns=headers)

    for row in rows:

        row_data = [x.text.strip() for x in row.find_all('td')]

        # workaround for incompatibility with pandas 23
        if len(row_data) != len(headers):
            print("Row length doesn't match header length. Skipping row.")
            logging.warning("Row length doesn't match header length. Skipping row.")
            continue

        s = pd.Series(row_data, index=headers)
        d = pd.DataFrame(s).T
        df = pd.concat([df, d], ignore_index=True)

    return df


def get_team_list(base_url, year, team_ids):
    """ Get the list of teams and their respective links from the leaders page.

    :param base_url: Base URL for the NACC baseball page
    :param year: The year eg "2016-17"
    :param team_ids: Dictionary of team names and abbreviations
    :returns: A list of dictionaries that includes the team name, abbr, and URL
    """
    soup = get_soup("{}{}/leaders".format(base_url, year))

    # search the page for the target element
    target = soup.find_all("table", {"class": "teamSummary"})
    logging.debug("Found %d target elements", len(target))
    if not len(target) == 1:
        print("Could not find exactly one target element")  # throw an exception?
        logging.critical("Could not find exactly one target element.")
        sys.exit(1)

    # create a list of links that are children of the target element
    links = [link for link in target[0].find_all('a') if 'href' in link.attrs]

    # create list of dicts
    # including team name, abbreviation, and url
    teamList = []
    for link in links:
        teamList.append({
            'team': get_text(link),
            'id': team_ids[get_text(link)],
            'url': get_href(link)
        })
    return teamList


# ****************************
# ***** Helper Functions *****
# ****************************

def to_int(x):
    if x is None:
        return None
    else:
        return int(x)


def to_float(x):
    if x is None:
        return None
    else:
        return float(x)


def to_none(x):
    if x == '':
        return None
    else:
        return x


def replace_dash(x, replacement):
    if x == '-':
        return replacement
    else:
        return x


def replace_inf(x, replacement):
    if x and x.lower() == 'inf':
        return replacement
    else:
        return x


def strip_dots(x):
    return x.rstrip('.')
