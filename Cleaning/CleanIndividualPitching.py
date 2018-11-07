""" This script is used to clean individual pitching data and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import CleanFunctions as cf
import utils
import metrics

SPLIT = "overall"


if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)

    conn = utils.connect_db(config)
    data = pd.read_sql_table("raw_pitchers_{}".format(SPLIT), conn)
    corrections = pd.read_sql_table("name_corrections", conn)
    conn.close()

    data = cf.normalize_names(data)
    data = cf.apply_corrections(data, corrections)
    data.drop(columns=["name"], inplace=True)

    data["ip"] = data["ip"].apply(cf.convert_ip)
    data = metrics.basic_pitching_metrics(data)
    print(data)
