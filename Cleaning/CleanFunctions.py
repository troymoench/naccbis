""" This module provides functions used in the data cleaning process. """
# Standard library imports
# Third party imports
import pandas as pd
# Local imports


# ****************************
# ***** Name Corrections *****
# ****************************

def normalize_names(data, verbose=False):
    """ Normalize names by splitting into first name and last name.
    :param data: A DataFrame
    :param verbose: Print extra information to standard out?
    :returns: A DataFrame
    """
    # split each name into first name and last name
    data["fname"] = [x.split(" ")[0].strip() for x in data["name"]]
    data["lname"] = [" ".join(x.split(" ")[1:]).strip() for x in data["name"]]

    # remove periods from first name
    data["fname"] = [x.replace(".", "") for x in data["fname"]]
    return data


def apply_corrections(data, corrections, verbose=False):
    """ Apply name corrections
    :param data: A DataFrame of the data to be updated
    :param corrections: A DataFrame of the name corrections
    :param verbose: Print extra information to standard out?
    :returns: A DataFrame with the updated names
    """
    # Return a copy of the DataFrame instead of modifying
    data = data.copy()

    for i in range(len(corrections)):
        row = corrections.iloc[i]
        # print(row)
        need_update = pd.Series((data["fname"] == row["uc_fname"]) &
                                (data["lname"] == row["uc_lname"]) &
                                (data["team"] == row["uc_team"]) &
                                (data["season"] == row["uc_season"]))

        if need_update.sum() == 0:
            print("No update")
            continue
        if verbose:
            print("Row(s) to be updated:")
            print(data[need_update], "\n")

        # update first name and last name with corrections
        data.loc[need_update, 'fname'] = row["c_fname"]
        data.loc[need_update, 'lname'] = row["c_lname"]
    return data


# *******************************
# ****** Assign Player ID's *****
# *******************************

def create_id(fname, lname):
    '''Create a player ID from a first name and last name.
    String format: <first 5 characters of last name><first 2 characters of first name><01>
    The last two integer digits allow for the prevention of ID conflicts.
    To increment by an integer n, use add_n(player_id, n)

    NOTE: spaces, periods, and apostrophes are omitted
    '''
    fname = fname.lower()
    lname = lname.lower().replace(' ', '').replace('.', '').replace('\'', '')  # remove spaces, periods, and apostrophes

    if len(lname) > 5:
        lname = lname[0:5]
    if len(fname) > 2:
        fname = fname[0:2]

    return "{}{}01".format(lname, fname)


def add_n(player_id, n):
    '''Add an integer  to a player id
    e.g. add_n("engelcu01", 2) -> "engelcu03"
    '''
    num = int(player_id[-2:]) + int(n)
    num = str(num).zfill(2)
    return "{}{}".format(player_id[0:len(player_id)-2], num)
