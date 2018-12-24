""" This script is used to clean individual offense data and load into database """
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


class IndividualOffenseCleaner:
    """ ETL class for individual offense """

    def __init__(self, split, conn):
        self.split = split
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_batters_{}".format(self.split), self.conn)
        self.corrections = pd.read_sql_table("name_corrections", self.conn)

    def transform(self):
        self.data = cf.normalize_names(self.data)
        self.data = cf.apply_corrections(self.data, self.corrections)
        self.data.drop(columns=["name"], inplace=True)
        self.data = metrics.basic_offensive_metrics(self.data)
        cols = ["no", "fname", "lname", "team", "season", "yr", "pos", "g", "pa", "ab",
                "r", "h", "x2b", "x3b", "hr", "rbi", "bb", "so", "hbp", "tb", "xbh", "sf",
                "sh", "gdp", "sb", "cs", "go", "fo", "go_fo", "hbp_p", "bb_p", "so_p",
                "babip", "iso", "avg", "obp", "slg", "ops", "sar"]

        self.data.replace(pd.np.inf, pd.np.nan, inplace=True)
        self.data = self.data[cols]

    def load(self):
        self.data.to_sql("batters_{}".format(self.split), self.conn, if_exists="append", index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)

    conn = utils.connect_db(config)
    cleaner = IndividualOffenseCleaner(SPLIT, conn)
    cleaner.run()
    conn.close()
