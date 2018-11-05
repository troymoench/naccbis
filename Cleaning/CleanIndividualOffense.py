""" This script is used to clean individual offense data and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import CleanFunctions as cf
import utils
import metrics


SPLIT = "conference"
OUTPUT = "csv"

if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)

    conn = utils.connect_db(config)

    data = pd.read_sql_table("raw_batters_{}".format(SPLIT), conn)
    corrections = pd.read_sql_table("name_corrections", conn)
    # player_ids = pd.read_sql_table("player_id", conn)
    conn.close()

    data = cf.normalize_names(data)
    data = cf.apply_corrections(data, corrections)
    data.drop(columns=["name"], inplace=True)
    data = metrics.basic_offensive_metrics(data)
    print(data)
    # print(pd.merge(player_ids, data, on=["fname", "lname", "team", "season"]))
