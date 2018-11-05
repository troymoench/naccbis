""" This script is used to clean team offense data and load into database """
# Standard library imports
import json
# Third party imports
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
    data = pd.read_sql_table("raw_team_offense_{}".format(SPLIT), conn)
    conn.close()

    data.rename(columns={"name": "team"}, inplace=True)

    data = metrics.basic_offensive_metrics(data)
    print(data)
