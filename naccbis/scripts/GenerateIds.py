""" This script is used to generate player ids

\b
1. extract raw data from database
2. apply name corrections
3. generate player ids
4. load transformed data into database
"""
# Standard library imports
import os
from typing import List, Optional
# Third party imports
import click
import pandas as pd
# Local imports
from naccbis.Cleaning import CleanFunctions
from naccbis.Common import utils
from naccbis import __version__


def make_full_name(fname: str, lname: str) -> str:
    return "{} {}".format(fname, lname)


def update_id_conflicts(data: pd.DataFrame) -> pd.DataFrame:
    """ Update player id conflicts by incrementing the numeric part of the id

    :param data: A DataFrame
    :returns: DataFrame with updated player ids
    """
    data = data.copy()

    new_col: List[str] = []
    new_col_idx: List[int] = []
    for _, group in data.groupby("player_id"):
        if group["full_name"].nunique() != 1:
            # print(group)

            df_list = [item for _, item in group.groupby("full_name")]
            # sort by first season then by first team (alphabetically)
            df_list.sort(key=lambda x: (x["season"].min(), x["team"].min()))
            # print(df_list)
            for i, item in enumerate(df_list):
                new_col_idx.extend(item.index.values.tolist())
                new_col.extend(map(CleanFunctions.add_n, item["player_id"], [i] * len(item)))

    if len(new_col) != len(new_col_idx):
        print("Oops! Length of column doesn't match length of index")
        raise ValueError()

    # update conflicting ID's
    data.loc[new_col_idx, "player_id"] = new_col
    return data


def get_duplicates(conn: object) -> pd.DataFrame:
    """ Retrieve duplicate names from the database

    :param conn: Database connection object
    :returns: A DataFrame of duplicate names
    """
    query = """
    SELECT dn.fname, dn.lname, dn.team, dn.season, dn.id
    FROM duplicate_names dn
    LEFT OUTER JOIN (
        SELECT fname, lname, max(id)
        FROM duplicate_names
        GROUP BY lname, fname
    ) AS f
    ON dn.fname = f.fname
    AND dn.lname = f.lname
    WHERE f.max > 0
    ORDER BY 1, 2, 4, 5;
    """
    return pd.read_sql_query(query, conn)


def update_duplicates(data: pd.DataFrame, duplicates: pd.DataFrame) -> pd.DataFrame:
    """ Update the player id of duplicate names by incrementing the numeric part
    of the player id.

    :param data: A DataFrame
    :param duplicates: A DataFrame of duplicate names
    :returns:
    """
    temp = pd.merge(data, duplicates, on=["fname", "lname", "team", "season"], how="outer")
    # merge is converting the id column from int to float
    temp["id"] = temp["id"].fillna(0).astype(int)
    temp["player_id"] = list(map(CleanFunctions.add_n, temp["player_id"], temp["id"]))

    temp.drop(columns=["id"], inplace=True)
    return temp


def verify_unique_ids(unique_before: int, unique_after: int, duplicates: pd.DataFrame) -> bool:
    """ unique_after == unique_before + dupes

    :param unique_before: Number of unique ids before name deduplication
    :param unique_after: Number of unique ids after name deduplication
    :param duplicates: A DataFrame of duplicate names
    :returns: True if unique_after == unique_before + dupes, false otherwise
    """
    grouped = duplicates.groupby(["fname", "lname"]).max()
    dupes = grouped["id"].sum()
    return unique_after == (unique_before + dupes)


def generate_ids(data: pd.DataFrame, duplicates: pd.DataFrame) -> pd.DataFrame:
    """ Generate player ids

    :param data: A DataFrame
    :param duplicates: A DataFrame of duplicate names
    :returns: A DataFrame with player ids
    """
    print("Generating player ids")
    data["player_id"] = list(map(CleanFunctions.create_id, data["fname"], data["lname"]))
    print("Unique ID's:", data["player_id"].nunique())

    data["full_name"] = list(map(make_full_name, data["fname"], data["lname"]))
    print("Unique names:", data["full_name"].nunique())
    data = update_id_conflicts(data)
    num_unique_before = data["player_id"].nunique()
    print("Unique ID's:", num_unique_before)

    print("Duplicate player-seasons to be updated:", duplicates["id"].sum())

    data = update_duplicates(data, duplicates)

    num_unique_after = data["player_id"].nunique()
    print("Unique ID's after:", num_unique_after)

    if verify_unique_ids(num_unique_before, num_unique_after, duplicates):
        print("Player ids verified successfully")
    else:
        print("An issue occurred while verifying player ids")
        raise ValueError("Player ID verification")
    data.drop(columns=["full_name"], inplace=True)
    return data


@click.command(help=__doc__)
@click.version_option(version=__version__, message='naccbis %(version)s')
@click.option("--load", is_flag=True, help="Load data into database")
@click.option("--clear", is_flag=True, help="Clear the database table before loading")
@click.option("--season", type=int, help="Filter output by season")
@click.option("--dir", type=str, default="", help="Directory to save the output to")
def cli(load: bool, clear: bool, season: Optional[int], dir: str) -> None:
    """ Script entry point """

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    corrections = pd.read_sql_table("name_corrections", conn)
    duplicates = get_duplicates(conn)

    batters = CleanFunctions.normalize_names(batters)
    pitchers = CleanFunctions.normalize_names(pitchers)

    batters = batters[["lname", "fname", "team", "season"]]
    pitchers = pitchers[["lname", "fname", "team", "season"]]

    # All batters and pitchers
    # (remove duplicates where a player batted and pitched in the same season)
    data = pd.merge(batters, pitchers, on=["fname", "lname", "team", "season"], how="outer")
    data = data.sort_values(by=["lname", "fname", "team", "season"])

    data = CleanFunctions.apply_corrections(data, corrections)
    data = generate_ids(data, duplicates)

    if season:
        data = data[data["season"] == season]

    if load:
        if clear:
            print("Clearing database table")
            conn.execute("DELETE FROM player_id")

        print("Loading data into database")
        utils.db_load_data(data, "player_id", conn, if_exists="append", index=False)

    else:
        print("Dumping to csv")
        data.to_csv(os.path.join(dir, "player_id.csv"), index=False)
    conn.close()


if __name__ == "__main__":
    cli()  # pragma: no cover
