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

    data = cf.normalize_names(data)
    data = cf.apply_corrections(data, corrections)
    data.drop(columns=["name"], inplace=True)

    data["ip"] = data["ip"].apply(cf.convert_ip)
    data = metrics.basic_pitching_metrics(data, conference=(SPLIT == "conference"))
    data.replace(pd.np.inf, pd.np.nan, inplace=True)
    if SPLIT == "overall":
        columns = ['no', 'fname', 'lname', 'team', 'season', 'yr', 'pos', 'g', 'gs',
                   'w', 'l', 'sv', 'cg', 'sho', 'ip', 'h', 'r', 'er', 'bb', 'so',
                   'x2b', 'x3b', 'hr', 'ab', 'wp', 'hbp', 'bk', 'sf', 'sh', 'pa',
                   'hbp_p', 'bb_p', 'so_p', 'iso', 'babip', 'avg', 'obp', 'slg', 'ops',
                   'lob_p', 'era', 'ra_9', 'so_9', 'bb_9', 'hr_9', 'whip']
    if SPLIT == "conference":
        columns = ['no', 'fname', 'lname', 'team', 'season', 'yr', 'pos', 'g', 'gs',
                   'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb', 'so', 'so_9',
                   'hr', 'era', 'ra_9', 'bb_9', 'hr_9', 'whip']
    data = data[columns]
    # print(data.info())
    data.to_sql("pitchers_{}".format(SPLIT), conn, if_exists="append", index=False)
    conn.close()
