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


class TeamPichingCleaner:
    """ ETL class for team pitching """
    VALID_SPLITS = ["overall", "conference"]

    def __init__(self, split, conn):
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_team_pitching_{}".format(self.split), self.conn)

    def transform(self):
        self.data["ip"] = self.data["ip"].apply(cf.convert_ip)
        conference = (self.split == "conference")
        self.data = metrics.basic_pitching_metrics(self.data, conference=conference)

    def load(self):
        self.data.to_sql("team_pitching_{}".format(self.split), self.conn, if_exists="append", index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":
    with open('../config.json') as f:
        config = json.load(f)
    utils.init_logging()
    conn = utils.connect_db(config)
    cleaner = TeamPichingCleaner(SPLIT, conn)
    cleaner.run()
    conn.close()
