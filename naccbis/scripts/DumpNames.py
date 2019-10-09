""" This script used to identify inconsistencies with player names.
These inconsistencies include, but are not limited to:
1. Typos
2. Name changes
3. Nicknames
"""
# Standard library imports
import argparse
# Third party imports
import pandas as pd
from Levenshtein import distance
# Local imports
import naccbis.Cleaning.CleanFunctions as cf
import naccbis.Common.utils as utils


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


def nickname_analysis(data, nicknames):
    """ Perform a nickname analysis on first names.
    This is used for identifying inconsistencies due to nicknames.
    :param data: A DataFrame
    :param nicknames: Nickname lookup table. A DataFrame.
    :returns: A DataFrame with player-season pairs with a matching name and
            nickname in the lookup table.
    """
    names = pd.DataFrame(data[["lname", "fname", "team", "season"]])

    # Compute the cartesian product
    cart_prod = pd.merge(names, names, on="lname")
    cart_prod = cart_prod[cart_prod["fname_x"] != cart_prod["fname_y"]]

    output = pd.merge(cart_prod, nicknames, left_on=["fname_x", "fname_y"],
                      right_on=["name", "nickname"])
    return output


def duplicate_names_analysis(data):
    """ Perform duplicate names analysis.
    :param data: A DataFrame
    :returns: A DataFrame with player-seasons that have the same name but
            different teams.
    """
    names = pd.DataFrame(data[["fname", "lname", "team", "season"]])
    names["name"] = [" ".join(x) for x in zip(names["fname"], names["lname"])]
    names = names[["name", "team", "season"]]

    temp = names[["name", "team"]].groupby(["name", "team"]).head(1)
    temp = temp.groupby(["name"]).filter(lambda x: len(x) > 1)
    output = names[names["name"].isin(temp["name"])].groupby(["name", "team", "season"]).head(1)
    output["fname"] = [x.split(" ")[0].strip() for x in output["name"]]
    output["lname"] = [" ".join(x.split(" ")[1:]).strip() for x in output["name"]]

    return output[["fname", "lname", "team", "season"]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DumpNames.py")
    parser.add_argument("-c", "--corrections", action="store_true",
                        help="Apply existing name corrections")
    parser.add_argument("-f", "--fname", type=int, metavar="FNAME",
                        help="Filter first names by a Levenshtein distance")
    parser.add_argument("-l", "--lname", type=int, metavar="LNAME",
                        help="Filter last names by a Levenshtein distance")
    parser.add_argument("--nicknames", action="store_true",
                        help="Perform a nickname analysis")
    parser.add_argument("--duplicates", action="store_true",
                        help="Perform duplicate names analysis")
    args = parser.parse_args()
    levenshtein_first = args.fname
    levenshtein_last = args.lname

    CSV_DIR = "csv/"

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    if args.corrections:
        corrections = pd.read_sql_table("name_corrections", conn)
    if args.nicknames:
        nicknames = pd.read_sql_table("nicknames", conn)

    conn.close()

    batters = cf.normalize_names(batters, verbose=True)
    pitchers = cf.normalize_names(pitchers, verbose=True)

    batters = batters[["lname", "fname", "team", "season", "pos"]]
    pitchers = pitchers[["lname", "fname", "team", "season", "pos"]]

    # All batters and pitchers
    data = pd.concat([batters, pitchers], ignore_index=True)
    data = data.sort_values(by=["lname", "fname", "team", "season"])
    # print(data)
    # print(corrections)

    if args.corrections:
        # apply name corrections
        data = cf.apply_corrections(data, corrections, verbose=True)
        data = data.sort_values(by=["lname", "fname", "team", "season"])

    if levenshtein_last or levenshtein_first:
        print("Performing levenshtein analysis")
        output = levenshtein_analysis(data, levenshtein_first, levenshtein_last)
        print("Found", len(output), "candidates. Dumping to csv")
        output.to_csv(CSV_DIR + "levenshtein_analysis.csv", index=False)

    if args.nicknames:
        print("Performing nickname analysis")
        output = nickname_analysis(data, nicknames)
        print("Found", len(output), "candidates. Dumping to csv")
        output.to_csv(CSV_DIR + "nickname_analysis.csv", index=False)

    if args.duplicates:
        print("Performing duplicate names analysis")
        output = duplicate_names_analysis(data)
        print("Found", len(output), "candidates. Dumping to csv")
        output.to_csv(CSV_DIR + "duplicate_names_analysis.csv", index=False)

    # dump all names
    print("Dumping all names to csv")
    data.to_csv(CSV_DIR + "all_names.csv", index=False)
