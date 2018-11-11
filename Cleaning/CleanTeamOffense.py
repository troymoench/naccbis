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
    utils.init_logging()

    conn = utils.connect_db(config)
    data = pd.read_sql_table("raw_team_offense_{}".format(SPLIT), conn)

    # data.rename(columns={"name": "team"}, inplace=True)

    data = metrics.basic_offensive_metrics(data)
    columns = ["name", "season", "g", "pa", "ab", "r", "h", "x2b", "x3b", "hr", "rbi",
               "bb", "so", "hbp", "tb", "xbh", "sf", "sh", "gdp", "sb", "cs", "go", "fo",
               "go_fo", "hbp_p", "bb_p", "so_p", "iso", "babip", "avg", "obp", "slg",
               "ops", "sar"]

    data[columns].to_sql("team_offense_{}".format(SPLIT), conn, if_exists="append", index=False)
    conn.close()
