"""This script used to identify inconsistencies with player names.
These inconsistencies include, but are not limited to:
1. Typos
2. Name changes
3. Nicknames
"""
# Standard library imports
import os
# Third party imports
import click
import pandas as pd
from Levenshtein import distance
# Local imports
from naccbis.Cleaning import CleanFunctions
from naccbis.Common import utils
from naccbis import __version__


def levenshtein_analysis(data: pd.DataFrame, lev_first: int, lev_last: int) -> pd.DataFrame:
    """ Perform a Levenshtein analysis on first names and last names.
    This is used for identifying typos.

    :param data: A DataFrame
    :param lev_first: Levenshtein distance between first names
    :param lev_last: Levenshtein distance between last names
    :returns: A DataFrame with player-season pairs that meet the filter parameters
    """
    # Get unique last names
    names = pd.DataFrame(data["lname"].unique())
    names["key"] = 0

    # Compute the cartesian product
    cart_prod = pd.merge(names, names, on="key")
    cart_prod.drop(columns=["key"], inplace=True)
    cart_prod.columns = ["lname1", "lname2"]

    # Compute the Levenshtein distance between each pair of names
    cart_prod["levenshtein"] = list(map(distance, cart_prod["lname1"], cart_prod["lname2"]))
    cart_prod = cart_prod[cart_prod.levenshtein == lev_last]

    output = pd.merge(data, cart_prod, left_on="lname", right_on="lname1")

    output = pd.merge(output, data, left_on="lname2", right_on="lname", how="inner")

    output["levenshtein_first"] = list(map(distance, output["fname_x"], output["fname_y"]))
    output = output[output["levenshtein_first"] == lev_first]

    output = output.sort_values(by=["levenshtein", "lname1"])
    return output


def nickname_analysis(data: pd.DataFrame, nicknames: pd.DataFrame) -> pd.DataFrame:
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

    return pd.merge(cart_prod,
                    nicknames,
                    left_on=["fname_x", "fname_y"],
                    right_on=["name", "nickname"])


def duplicate_names_analysis(data: pd.DataFrame) -> pd.DataFrame:
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
    output = names[names["name"].isin(temp["name"])].\
        groupby(["name", "team", "season"]).head(1)
    output["fname"] = output["name"].apply(CleanFunctions.split_fname)
    output["lname"] = output["name"].apply(CleanFunctions.split_lname)

    return output[["fname", "lname", "team", "season"]]


@click.command(help="Identify inconsistencies with player names")
@click.version_option(version=__version__, message='naccbis %(version)s')
@click.option("-c", "--corrections", is_flag=True, help="Apply existing name corrections")
@click.option(
    "-f", "--fname", type=int, default=0, show_default=True,
    help="Filter first names by a Levenshtein distance"
)
@click.option(
    "-l", "--lname", type=int, default=0, show_default=True,
    help="Filter last names by a Levenshtein distance"
)
@click.option("--nicknames", is_flag=True, help="Perform a nickname analysis")
@click.option("--duplicates", is_flag=True, help="Perform duplicate names analysis")
@click.option("--dir", type=str, default="", help="Directory to save the output to")
def cli(
    corrections: bool, fname: int, lname: int, nicknames: bool,
    duplicates: bool, dir: str
) -> None:
    """ Script entry point """
    levenshtein_first = fname
    levenshtein_last = lname
    print(fname, lname)
    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    if corrections:
        corrections_df = pd.read_sql_table("name_corrections", conn)
    if nicknames:
        nicknames_df = pd.read_sql_table("nicknames", conn)

    conn.close()

    batters = CleanFunctions.normalize_names(batters)
    pitchers = CleanFunctions.normalize_names(pitchers)

    batters = batters[["lname", "fname", "team", "season", "pos"]]
    pitchers = pitchers[["lname", "fname", "team", "season", "pos"]]

    data = pd.concat([batters, pitchers], ignore_index=True)
    data = data.sort_values(by=["lname", "fname", "team", "season"])

    if corrections:
        data = CleanFunctions.apply_corrections(data, corrections_df)
        data = data.sort_values(by=["lname", "fname", "team", "season"])

    if levenshtein_last or levenshtein_first:
        print("Performing levenshtein analysis")
        output = levenshtein_analysis(data, levenshtein_first, levenshtein_last)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = os.path.join(dir, "levenshtein_analysis.csv")
            output.to_csv(filename, index=False)

    if nicknames:
        print("Performing nickname analysis")
        output = nickname_analysis(data, nicknames_df)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = os.path.join(dir, "nickname_analysis.csv")
            output.to_csv(filename, index=False)

    if duplicates:
        print("Performing duplicate names analysis")
        output = duplicate_names_analysis(data)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = os.path.join(dir, "duplicate_names_analysis.csv")
            output.to_csv(filename, index=False)

    print("Dumping all names to csv")
    filename = os.path.join(dir, "all_names.csv")
    data.to_csv(filename, index=False)


if __name__ == "__main__":
    cli()  # pragma: no cover
