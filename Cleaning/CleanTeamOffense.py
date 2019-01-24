""" This script is used to clean team offense data and load into database """
# Standard library imports
import argparse
import os
# Third party imports
import pandas as pd
# Local imports
import Common.metrics as metrics
import Common.utils as utils


class TeamOffenseETL:
    """ ETL class for team offense """
    VALID_SPLITS = ["overall", "conference"]
    CSV_DIR = "csv/"

    def __init__(self, year, split, load_db, conn):
        self.year = year
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.load_db = load_db
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_team_offense_{}".format(self.split), self.conn)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]

    def transform(self):
        self.data = metrics.basic_offensive_metrics(self.data)
        columns = ["name", "season", "g", "pa", "ab", "r", "h", "x2b", "x3b", "hr", "rbi",
                   "bb", "so", "hbp", "tb", "xbh", "sf", "sh", "gdp", "sb", "cs", "go", "fo",
                   "go_fo", "hbp_p", "bb_p", "so_p", "iso", "babip", "avg", "obp", "slg",
                   "ops", "sar"]
        self.data = self.data[columns]

    def load(self):
        table_name = "team_offense_{}".format(self.split)
        if self.load_db:
            print("Loading data into database")
            utils.db_load_data(self.data, table_name, self.conn, if_exists="append", index=False)
        else:
            print("Dumping to csv")
            self.data.to_csv(os.path.join(self.CSV_DIR, "{}.csv".format(table_name)), index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract, Transform, Load Team Offense data")
    parser.add_argument("--year", type=int, default=None, help="Filter by year")
    parser.add_argument("--split", type=str, default="overall", help="Filter by split")
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    args = parser.parse_args()

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])
    team_offense = TeamOffenseETL(args.year, args.split, args.load, conn)
    team_offense.run()
    conn.close()
