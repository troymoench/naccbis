""" This script is used to clean individual pitching data and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import CleanFunctions as cf
import metrics
import utils

SPLIT = "overall"


class IndividualPitchingETL:
    """ ETL class for individual pitching """
    VALID_SPLITS = ["overall", "conference"]

    def __init__(self, split, conn):
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_pitchers_{}".format(self.split), self.conn)
        self.corrections = pd.read_sql_table("name_corrections", self.conn)

    def transform(self):
        self.data = cf.normalize_names(self.data)
        self.data = cf.apply_corrections(self.data, self.corrections)
        self.data.drop(columns=["name"], inplace=True)

        self.data["ip"] = self.data["ip"].apply(cf.convert_ip)
        conference = (self.split == "conference")
        self.data = metrics.basic_pitching_metrics(self.data, conference=conference)
        self.data.replace(pd.np.inf, pd.np.nan, inplace=True)
        if self.split == "overall":
            columns = ['no', 'fname', 'lname', 'team', 'season', 'yr', 'pos', 'g', 'gs',
                       'w', 'l', 'sv', 'cg', 'sho', 'ip', 'h', 'r', 'er', 'bb', 'so',
                       'x2b', 'x3b', 'hr', 'ab', 'wp', 'hbp', 'bk', 'sf', 'sh', 'pa',
                       'hbp_p', 'bb_p', 'so_p', 'iso', 'babip', 'avg', 'obp', 'slg', 'ops',
                       'lob_p', 'era', 'ra_9', 'so_9', 'bb_9', 'hr_9', 'whip']
        if self.split == "conference":
            columns = ['no', 'fname', 'lname', 'team', 'season', 'yr', 'pos', 'g', 'gs',
                       'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb', 'so', 'so_9',
                       'hr', 'era', 'ra_9', 'bb_9', 'hr_9', 'whip']
        self.data = self.data[columns]

    def load(self):
        self.data.to_sql("pitchers_{}".format(self.split), conn, if_exists="append", index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)
    utils.init_logging()
    conn = utils.connect_db(config)
    individual_pitching = IndividualPitchingETL(SPLIT, conn)
    individual_pitching.run()
    conn.close()
