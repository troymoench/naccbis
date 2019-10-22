""" This script is used to generate player ids """
# Standard library imports
import argparse
import sys
# Third party imports
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
# Local imports
import naccbis.Cleaning.CleanFunctions as cf
import naccbis.Common.utils as utils


def make_full_name(fname, lname):
    return "{} {}".format(fname, lname)


def update_id_conflicts(data):
    """ Update player id conflicts by incrementing the numeric part of the id
    :param data: A DataFrame
    :returns: DataFrame with updated player ids
    """
    data = data.copy()

    new_col = []
    new_col_idx = []
    for _, group in data.groupby("player_id"):
        if group["full_name"].nunique() != 1:
            # print(group)

            df_list = [item for _, item in group.groupby("full_name")]
            # sort by first season then by first team (alphabetically)
            df_list.sort(key=lambda x: (x["season"].min(), x["team"].min()))
            # print(df_list)
            for i, item in enumerate(df_list):
                new_col_idx.extend(item.index.values.tolist())
                new_col.extend(map(cf.add_n, item["player_id"], [i] * len(item)))

    if len(new_col) != len(new_col_idx):
        print("Oops! Length of column doesn't match length of index")
        sys.exit(1)

    # update conflicting ID's
    data.loc[new_col_idx, "player_id"] = new_col
    return data


def get_duplicates(conn):
    """ Retrieve duplicate names from the database
    :param conn: Database connection object
    :returns: A DataFrame of duplicate names
    """
    query = "select dn.fname, dn.lname, dn.team, dn.season, dn.id from duplicate_names dn " \
            "left outer join (select fname, lname, max(id) from duplicate_names group by lname, fname) " \
            "as f on dn.fname = f.fname and dn.lname = f.lname where f.max > 0 order by 1, 2, 4, 5;"
    # query = "select dn.fname||' '||dn.lname as name, dn.team, dn.season, dn.id from duplicate_names dn" \
    #         " left outer join (select fname, lname, max(id) from duplicate_names group by lname, fname) as f" \
    #         " on dn.fname = f.fname and dn.lname = f.lname where f.max > 0 order by 1, 3, 4;"

    duplicates = pd.read_sql_query(query, conn)
    return duplicates


def update_duplicates(data, duplicates):
    """ Update the player id of duplicate names by incrementing the numeric part
    of the player id.
    :param data: A DataFrame
    :param duplicates: A DataFrame of duplicate names
    :returns:
    """
    temp = pd.merge(data, duplicates, on=["fname", "lname", "team", "season"], how="outer")
    # merge is converting the id column from int to float
    temp["id"] = temp["id"].fillna(0).astype(int)
    temp["player_id"] = list(map(cf.add_n, temp["player_id"], temp["id"]))

    temp.drop(columns=["id"], inplace=True)
    return temp


def verify_unique_ids(unique_before, unique_after, duplicates):
    """ unique_after == unique_before + dupes
    :param unique_before: Number of unique ids before name deduplication
    :param unique_after: Number of unique ids after name deduplication
    :param duplicates: A DataFrame of duplicate names
    :returns: True if unique_after == unique_before + dupes, false otherwise
    """
    grouped = duplicates.groupby(["fname", "lname"])
    grouped = grouped.max()
    dupes = grouped["id"].sum()
    return unique_after == (unique_before + dupes)


def generate_ids(data, duplicates):
    """ Generate player ids
    :param data: A DataFrame
    :param duplicates: A DataFrame of duplicate names
    :returns: A DataFrame with player ids
    """
    print("Generating player ids")
    data["player_id"] = list(map(cf.create_id, data["fname"], data["lname"]))
    print("Unique ID's:", data["player_id"].nunique())

    data["full_name"] = list(map(make_full_name, data["fname"], data["lname"]))
    print("Unique names:", data["full_name"].nunique())
    data = update_id_conflicts(data)
    num_unique_before = data["player_id"].nunique()
    print("Unique ID's:", num_unique_before)
    # print(data)

    print("Duplicate player-seasons to be updated:", duplicates["id"].sum())

    data = update_duplicates(data, duplicates)

    num_unique_after = data["player_id"].nunique()
    print("Unique ID's after:", num_unique_after)

    if verify_unique_ids(num_unique_before, num_unique_after, duplicates):
        print("Player ids verified successfully")
    else:
        print("An issue occurred while verifying player ids")
        sys.exit(1)
    data.drop(columns=["full_name"], inplace=True)
    return data


if __name__ == "__main__":
    # extract raw data from database
    # apply name corrections
    # generate player ids
    # load transformed data into database
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    parser.add_argument("--dir", type=str, default="",
                        help="Directory to save the output to")
    args = parser.parse_args()

    CSV_DIR = args.dir

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    corrections = pd.read_sql_table("name_corrections", conn)
    duplicates = get_duplicates(conn)

    batters = cf.normalize_names(batters, verbose=True)
    pitchers = cf.normalize_names(pitchers, verbose=True)

    batters = batters[["lname", "fname", "team", "season"]]
    pitchers = pitchers[["lname", "fname", "team", "season"]]

    # All batters and pitchers
    # (remove duplicates where a player batted and pitched in the same season)
    data = pd.merge(batters, pitchers, on=["fname", "lname", "team", "season"], how="outer")
    data = data.sort_values(by=["lname", "fname", "team", "season"])

    data = cf.apply_corrections(data, corrections)

    data = generate_ids(data, duplicates)

    if args.load:
        print("Loading data into database")
        try:
            data.to_sql("player_id", conn, if_exists="append", index=False)
            # NOTE: May want to use if_exists="replace" along with specifying
            # the table schema
        except SQLAlchemyError as e:
            print("Failed to load data into database")
            print(e)
            conn.close()
            sys.exit(1)
        print("Loaded successfully")
    else:
        print("Dumping to csv")
        data.to_csv(CSV_DIR + "player_id.csv", index=False)
    conn.close()
