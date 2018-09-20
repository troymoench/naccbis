""" This script used to identify inconsistencies with player names.
These inconsistencies include, but are not limited to:
1. Typos
2. Name changes
3. Nicknames
"""

import pandas as pd
from sqlalchemy import create_engine
import json
import argparse
from Levenshtein import distance
import CleanFunctions


def levenshtein_analysis(data, levenshtein_first, levenshtein_last):
    """ Perform a Levenshtein analysis on first names and last names.
    This is used for identifying typos.
    :param data: A DataFrame
    :param levenshtein_first: Levenshtein distance between first names
    :param levenshtein_last: Levenshtein distance between last names
    :returns: A DataFrame with player-season pairs that meet the filter parameters
    """
    # Get unique last names
    names = pd.DataFrame(data["lname"].unique())
    names["key"] = 0
    # print(names)

    # Compute the cartesian product
    cart_prod = pd.merge(names, names, on="key")
    cart_prod.drop(columns=["key"], inplace=True)
    cart_prod.columns = ["lname1", "lname2"]
    # print(cart_prod)

    # names.drop(columns=["key"], inplace=True)
    # names.columns = ["lname"]

    # Compute the Levenshtein distance between each pair of names
    cart_prod["levenshtein"] = list(map(distance, cart_prod["lname1"], cart_prod["lname2"]))
    # cart_prod = cart_prod[(cart_prod.levenshtein == 1) | (cart_prod.levenshtein == 2)]
    cart_prod = cart_prod[cart_prod.levenshtein == levenshtein_last]

    output = pd.merge(data, cart_prod, left_on="lname", right_on="lname1")

    output = pd.merge(output, data, left_on="lname2", right_on="lname", how="inner")

    output["levenshtein_first"] = list(map(distance, output["fname_x"], output["fname_y"]))
    output = output[output["levenshtein_first"] == levenshtein_first]

    # output = output[output["fname_x"] == output["fname_y"]]
    output = output.sort_values(by=["levenshtein", "lname1"])
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DumpNames.py")
    parser.add_argument("-c", "--corrections", action="store_true",
                        help="Apply existing name corrections")
    parser.add_argument("-f", "--fname", type=int, metavar="FNAME",
                        help="Filter first names by a Levenshtein distance")
    parser.add_argument("-l", "--lname", type=int, metavar="LNAME",
                        help="Filter last names by a Levenshtein distance")
    args = parser.parse_args()
    levenshtein_first = args.fname
    levenshtein_last = args.lname

    with open('../config.json') as f:
        config = json.load(f)

    conn_str = 'postgresql+psycopg2://{}:{}@{}:5432/{}'.format(config["user"], config["password"], config["host"], config["database"])
    engine = create_engine(conn_str)
    conn = engine.connect()

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    if args.corrections:
        corrections = pd.read_sql_table("name_corrections", conn)

    conn.close()

    batters = CleanFunctions.normalize_names(batters, verbose=True)
    pitchers = CleanFunctions.normalize_names(pitchers, verbose=True)

    batters = batters[["lname", "fname", "team", "season", "pos"]]
    pitchers = pitchers[["lname", "fname", "team", "season", "pos"]]

    # All batters and pitchers
    data = pd.concat([batters, pitchers], ignore_index=True)
    data = data.sort_values(by=["lname", "fname", "team", "season"])
    # print(data)
    # print(corrections)

    if args.corrections:
        # apply name corrections
        data = CleanFunctions.apply_corrections(data, corrections, verbose=True)
        data = data.sort_values(by=["lname", "fname", "team", "season"])

    output = levenshtein_analysis(data, levenshtein_first, levenshtein_last)
    output.to_csv("output.csv", index=False)
