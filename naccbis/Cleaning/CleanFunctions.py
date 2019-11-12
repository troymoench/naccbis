""" This module provides functions used in the data cleaning process. """
# Standard library imports
import logging
# Third party imports
import pandas as pd
# Local imports


# ****************************
# ***** Name Corrections *****
# ****************************

def normalize_names(data):
    """ Normalize names by splitting into first name and last name.

    :param data: A DataFrame
    :returns: A DataFrame
    """
    # split each name into first name and last name
    data["fname"] = [x.split(" ")[0].strip() for x in data["name"]]
    data["lname"] = [" ".join(x.split(" ")[1:]).strip() for x in data["name"]]

    # remove periods from first name
    data["fname"] = [x.replace(".", "") for x in data["fname"]]
    return data


def apply_corrections(data, corrections):
    """ Apply name corrections

    :param data: A DataFrame of the data to be updated
    :param corrections: A DataFrame of the name corrections
    :returns: A DataFrame with the updated names
    """
    # Return a copy of the DataFrame instead of modifying
    data = data.copy()
    corrections = corrections.copy()
    # select only the columns we care about
    corrections = corrections[[
        "uc_fname",
        "uc_lname",
        "uc_team",
        "uc_season",
        "c_fname",
        "c_lname"]]
    corrections.rename(columns={
        "uc_fname": "fname",
        "uc_lname": "lname",
        "uc_team": "team",
        "uc_season": "season"
    }, inplace=True)
    data = pd.merge(data, corrections, how="left", on=["fname", "lname", "team", "season"])

    need_fname_update = ~data["c_fname"].isnull()
    need_lname_update = ~data["c_lname"].isnull()
    if need_fname_update.sum() == 0 and need_lname_update.sum() == 0:
        logging.info("No name corrections needed")
    else:
        logging.info("Row(s) to be updated:")
        logging.info(data[need_fname_update | need_lname_update])

    data.loc[need_fname_update, "fname"] = data["c_fname"].dropna()
    data.loc[need_lname_update, "lname"] = data["c_lname"].dropna()

    data.drop(columns=["c_fname", "c_lname"], inplace=True)

    return data


# *******************************
# ****** Assign Player ID's *****
# *******************************

def create_id(fname, lname):
    """Create a player ID from a first name and last name.
    String format: <first 5 characters of last name><first 2 characters of first name><01>
    The last two integer digits allow for the prevention of ID conflicts.
    To increment by an integer n, use add_n(player_id, n)

    NOTE: spaces, periods, and apostrophes are omitted
    """
    fname = fname.lower()
    # remove spaces, periods, and apostrophes
    lname = lname.lower().replace(' ', '').replace('.', '').replace('\'', '')

    if len(lname) > 5:
        lname = lname[0:5]
    if len(fname) > 2:
        fname = fname[0:2]

    return "{}{}01".format(lname, fname)


def add_n(player_id, n):
    """Add an integer to a player id
    e.g. add_n("engelcu01", 2) -> "engelcu03"
    """
    num = int(player_id[-2:]) + int(n)
    num = str(num).zfill(2)
    return "{}{}".format(player_id[0:len(player_id) - 2], num)

# ****************************
# ****** Misc. Functions *****
# ****************************


def convert_ip(ip_str):
    """ Convert innings pitched from the string representation to the float

    :param ip_str: String representation of innings pitched
    :returns: Float representation of innings pitched
    """
    temp = ip_str.split(".")
    return int(temp[0]) + int(temp[1]) * (1 / 3)
