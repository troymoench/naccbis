""" This module provides general scraping functions as well as
some utility functions used in the scraping process.
"""
# Standard library imports
import logging
import re
from time import sleep
from typing import Dict, List

# Third party imports
from bs4 import BeautifulSoup, element
import pandas as pd
import requests

# Local imports


# ********************************
# ** General Scraping Functions **
# ********************************
def get_soup(url: str, backoff: int = 1) -> BeautifulSoup:
    """Create a BeautifulSoup object from a web page with the requested URL

    :param url: A string with the requested URL
    :param backoff: Number of seconds to sleep to prevent overloading the server
    :returns: A BeautifulSoup object
    """
    logging.debug("Backing off for %f seconds", backoff)
    sleep(backoff)  # to prevent overloading the server
    logging.debug("GET " + url)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    }
    try:
        request = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        logging.critical("Error: Unable to connect to", url)
        raise
    text = request.text
    return BeautifulSoup(text, "html.parser")


def get_text(html_tag: element.Tag) -> str:
    """Get the inner HTML from a BeautifulSoup tag and strip whitespace.

    :param html_tag: BeautifulSoup tag
    :returns: The inner HTML as a string
    """
    return html_tag.text.strip()


def get_href(html_tag: element.Tag) -> str:
    """Get the href attribute from a BeautifulSoup tag

    :param html_tag: BeautifulSoup tag
    :returns: The href attribute as a string
    """
    return html_tag.attrs["href"]


def find_table(soup_obj: BeautifulSoup, header_values: List[str]) -> List[int]:
    """Find HTML tables that contain the specified header values.
    Note that header value matching is case insensitive.

    :param soup_obj: BeautifulSoup object to search
    :param header_values: A list of header values to search for
    :returns: A list of table indices. Returns an empty list if table not found.
    """
    header_values = [x.lower() for x in header_values]

    indices = []
    tables = soup_obj.find_all("table")
    for i, table in enumerate(tables):
        header = table.find_all("th")
        columns = [x.text.strip().lower() for x in header]
        if set(header_values).issubset(set(columns)):
            indices.append(i)
        else:
            missing_values = set(header_values) - set(columns)
            logging.debug("Missing values in table {}: {}".format(i, missing_values))
    logging.debug("Found %d tables with matching headers", len(indices))
    return indices


def scrape_table(
    soup: BeautifulSoup, tbl_num: int, first_row: int = 2, skip_rows: int = 0
) -> pd.DataFrame:
    """Scrape HTML table with the specified index and populate a DataFrame.

    :param soup: BeautifulSoup object containing the table
    :param tbl_num: Integer index that specifies the table to scrape. Note that
                    the index is 1 based.
    :param first_row: First table row that will populate the DataFrame
    :param skip_rows: Number of rows to skip on the bottom of the table
    :returns: A DataFrame of the raw scraped table
    """
    table = soup.find_all("table")[tbl_num - 1]
    html_th = table.find_all("th")
    headers = [x.text.strip() for x in html_th]

    html_rows = table.find_all("tr")
    rows = html_rows[first_row - 1 : len(html_rows) - skip_rows]
    logging.debug("Found %d table rows", len(rows))

    # Empty DataFrame to add rows to
    df = pd.DataFrame(columns=headers)

    for row in rows:

        row_data = [x.text.strip() for x in row.find_all("td")]

        # workaround for incompatibility with pandas 23
        if len(row_data) != len(headers):
            print("Row length doesn't match header length. Skipping row.")
            logging.warning("Row length doesn't match header length. Skipping row.")
            continue

        s = pd.Series(row_data, index=headers)
        d = pd.DataFrame(s).T
        df = pd.concat([df, d], ignore_index=True)

    return df


def get_team_list(
    base_url: str, year: str, team_ids: Dict[str, str]
) -> List[Dict[str, str]]:
    """Get the list of teams and their respective links from the leaders page.

    :param base_url: Base URL for the NACC baseball page
    :param year: The year eg "2016-17"
    :param team_ids: Dictionary of team names and abbreviations
    :returns: A list of dictionaries that includes the team name, abbr, and URL
    """
    soup = get_soup("{}{}/leaders".format(base_url, year))

    # search the page for the target element
    target = soup.find_all("h3", string="Player Stats by Team")[0].find_next_siblings(
        "ul"
    )
    logging.debug("Found %d target elements", len(target))
    if not len(target) == 1:
        logging.critical("Could not find exactly one target element.")
        raise ValueError("Could not find exactly one target element")

    # create a list of links that are children of the target element
    links = [link for link in target[0].find_all("a") if "href" in link.attrs]

    # create list of dicts
    # including team name, abbreviation, and url
    teamList = []
    for link in links:
        teamList.append(
            {
                "team": get_text(link),
                "id": team_ids[get_text(link)],
                "url": get_href(link),
            }
        )
    return teamList


def skip_team(soup: BeautifulSoup) -> bool:
    """Skip team if no players meet the minimum

    :param soup: BeautifulSoup object for a team
    :returns: True if the team should be skipped, False otherwise
    """
    pattern = re.compile("No players meet the minimum")
    skip = len(soup.find_all(string=pattern)) > 0
    if skip:
        logging.warning("No players meet the minimum. Skipping team")
    return skip
