""" This script is used to clean team offense data and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import metrics
import utils

SPLIT = "overall"
OUTPUT = "csv"


class TeamOffenseCleaner:
    """ ETL class for team offense """
    VALID_SPLITS = ["overall", "conference"]

    def __init__(self, split, conn):
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_team_offense_{}".format(self.split), self.conn)

    def transform(self):
        self.data = metrics.basic_offensive_metrics(self.data)
        columns = ["name", "season", "g", "pa", "ab", "r", "h", "x2b", "x3b", "hr", "rbi",
                   "bb", "so", "hbp", "tb", "xbh", "sf", "sh", "gdp", "sb", "cs", "go", "fo",
                   "go_fo", "hbp_p", "bb_p", "so_p", "iso", "babip", "avg", "obp", "slg",
                   "ops", "sar"]
        self.data = self.data[columns]

    def load(self):
        self.data.to_sql("team_offense_{}".format(self.split), self.conn, if_exists="append", index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)
    utils.init_logging()
    conn = utils.connect_db(config)
    cleaner = TeamOffenseCleaner(SPLIT, conn)
    cleaner.run()
    conn.close()
