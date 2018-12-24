""" This script is used to clean team pitching data and load into database """
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
    utils.init_logging()

    conn = utils.connect_db(config)
    data = pd.read_sql_table("raw_team_pitching_{}".format(SPLIT), conn)
    data["ip"] = data["ip"].apply(cf.convert_ip)
    data = metrics.basic_pitching_metrics(data, conference=(SPLIT == "conference"))
    # print(data.info())
    data.to_sql("team_pitching_{}".format(SPLIT), conn, if_exists="append", index=False)
    conn.close()
