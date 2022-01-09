""" This module provides functions used in the data cleaning process. """
# Standard library imports
import logging

# Third party imports
import pandas as pd

# Local imports


def split_fname(name: str) -> str:
    return name.split(" ")[0].strip()


def split_lname(name: str) -> str:
    return " ".join(name.split(" ")[1:]).strip()


def normalize_names(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize names by splitting into first name and last name.

    :param data: A DataFrame
    :returns: A DataFrame
    """
    data["fname"] = data["name"].apply(split_fname)
    data["lname"] = data["name"].apply(split_lname)

    data["fname"] = data["fname"].str.replace(".", "", regex=False)
    return data


def apply_corrections(data: pd.DataFrame, corrections: pd.DataFrame) -> pd.DataFrame:
    """Apply name corrections

    :param data: A DataFrame of the data to be updated
    :param corrections: A DataFrame of the name corrections
    :returns: A DataFrame with the updated names
    """
    data = data.copy()
    corrections = corrections.copy()
    corrections = corrections[
        ["uc_fname", "uc_lname", "uc_team", "uc_season", "c_fname", "c_lname"]
    ]
    corrections.rename(
        columns={
            "uc_fname": "fname",
            "uc_lname": "lname",
            "uc_team": "team",
            "uc_season": "season",
        },
        inplace=True,
    )
    data = pd.merge(
        data, corrections, how="left", on=["fname", "lname", "team", "season"]
    )

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


def create_id(fname: str, lname: str) -> str:
    """Create a player ID from a first name and last name.
    String format: <first 5 characters of last name><first 2 characters of first name><01>
    The last two integer digits allow for the prevention of ID conflicts.
    To increment by an integer n, use add_n(player_id, n)

    NOTE: spaces, periods, and apostrophes are omitted
    """
    fname = fname.lower()
    lname = lname.lower()
    for char in " .'":
        lname = lname.replace(char, "")

    if len(lname) > 5:
        lname = lname[0:5]
    if len(fname) > 2:
        fname = fname[0:2]

    return f"{lname}{fname}01"


def add_n(player_id: str, n: int) -> str:
    """Add an integer to a player id
    e.g. add_n("engelcu01", 2) -> "engelcu03"
    """
    temp = int(player_id[-2:]) + n
    num = str(temp).zfill(2)
    return f"{player_id[:-2]}{num}"


def convert_ip(ip_str: str) -> float:
    """Convert innings pitched from the string representation to the float

    :param ip_str: String representation of innings pitched
    :returns: Float representation of innings pitched
    """
    innings, outs = ip_str.split(".")
    return int(innings) + int(outs) * (1 / 3)
