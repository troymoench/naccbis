""" This script is used to clean individual offense data and load into database """
# Standard library imports
import json
# Third party imports
import numpy as np
import pandas as pd
# Local imports
import CleanFunctions as cf
import utils
import metrics


SPLIT = "overall"
OUTPUT = "csv"

if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)

    conn = utils.connect_db(config)

    data = pd.read_sql_table("raw_batters_{}".format(SPLIT), conn)
    corrections = pd.read_sql_table("name_corrections", conn)
    # player_ids = pd.read_sql_table("player_id", conn)

    data = cf.normalize_names(data)
    data = cf.apply_corrections(data, corrections)
    data.drop(columns=["name"], inplace=True)
    data = metrics.basic_offensive_metrics(data)
    # print(data)
    # print(data.columns.tolist())
    cols = ["no", "fname", "lname", "team", "season", "yr", "pos", "g", "pa", "ab",
            "r", "h", "x2b", "x3b", "hr", "rbi", "bb", "so", "hbp", "tb", "xbh", "sf",
            "sh", "gdp", "sb", "cs", "go", "fo", "go_fo", "hbp_p", "bb_p", "so_p",
            "babip", "iso", "avg", "obp", "slg", "ops", "sar"]

    data.replace(np.inf, np.nan, inplace=True)
    # print(pd.merge(player_ids, data, on=["fname", "lname", "team", "season"]))

    data[cols].to_sql("batters_{}".format(SPLIT), conn, if_exists="append", index=False)
    conn.close()
