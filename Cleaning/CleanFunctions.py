""" This module provides functions used in the data cleaning process. """
import pandas as pd
import json


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
        # if need_update.sum() > 1:
        #     print("Must update one row at a time!")
        #     exit(1)
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


def set_ids(data, file, verbose=False):
    '''Set the Player ID's
    Player ID format is the same as Baseball Reference and the Lahman Database
    '''

    # initialize ID's

    data["id"] = list(map(create_id, data["fname"], data["lname"]))
    if verbose:
        print("Unique ID's before: ", data["id"].nunique())

    # fix ID conflicts
    if verbose:
        print("Fixing ID conflicts")

    data["full_name"] = list(map((lambda x, y: "{} {}".format(x, y)), data["fname"], data["lname"]))
    if verbose:
        print("Unique names: ", data["full_name"].nunique())

    new_col = []
    new_col_idx = []
    for _, group in data.groupby("id"):
        if group["full_name"].nunique() != 1:
            # print(group["full_name"].unique())
            df_list = [group[group["full_name"] == name] for name in group["full_name"].unique()]

            # sort by first season then by first team (alphabetically)
            df_list.sort(key=lambda x: x["season"].min())  # this only sorts by first season (quick and dirty)
            # TODO: Sort by first season AND by first team (alphabetically)

            for i, item in enumerate(df_list):
                new_col_idx.extend(item.index.values.tolist())
                new_col.extend(map(add_n, item["id"], [i] * len(item)))

    if len(new_col) != len(new_col_idx):
        print("Oops! Length of column doesn't match length of index")
        exit(1)

    # update conflicting ID's
    data.loc[new_col_idx, "id"] = new_col

    if verbose:
        print("Unique ID's after: ", data["id"].nunique())

    # ****************
    # ** Same Names **
    # ****************

    if verbose:
        print("Fixing Same Names")

    # import same names

    with open(file) as f:
        same_names = json.load(f)

    for same_name in same_names["same_names"]:
        df_list = []
        for team in same_name["teams"]:
            idx_list = []  # create list of indices of matching rows
            for season in team["seasons"]:
                selection = (data["fname"] == same_name["fname"]) & \
                            (data["lname"] == same_name["lname"]) & \
                            (data["team"] == team["team"]) & \
                            (data["season"] == season)
                idx_list.extend(data.loc[selection].index.values.tolist())
            df = data.loc[idx_list]
            df_list.append(df)

        # sort by first season then by first team (alphabetically)
        df_list.sort(key=lambda x: x["season"].min())  # this only sorts by first season (quick and dirty)
        # TODO: Sort by first season AND by first team (alphabetically)

        new_col_idx = []
        new_col = []
        for i, item in enumerate(df_list):
            new_col_idx.extend(item.index.values.tolist())
            new_col.extend(map(add_n, item["id"], [i] * len(item)))

        if len(new_col) != len(new_col_idx):
            print("Oops! Length of column doesn't match length of index")
            exit(1)
        # update conflicting ID's
        data.loc[new_col_idx, "id"] = new_col

    if verbose:
        print("Unique ID's after: ", data["id"].nunique())

    data.drop(columns=["full_name"], inplace=True)
    return data
