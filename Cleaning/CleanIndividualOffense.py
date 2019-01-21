""" This script is used to clean individual offense data and load into database """
# Standard library imports
import argparse
import json
import os
# Third party imports
import pandas as pd
# Local imports
import CleanFunctions as cf
import Common.utils as utils
import Common.metrics as metrics


class IndividualOffenseETL:
    """ ETL class for individual offense """
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
        self.data = pd.read_sql_table("raw_batters_{}".format(self.split), self.conn)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]
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
        table_name = "batters_{}".format(self.split)
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
    parser = argparse.ArgumentParser(description="Extract, Transform, Load Individual Offense data")
    parser.add_argument("--year", type=int, default=None, help="Filter by year")
    parser.add_argument("--split", type=str, default="overall", help="Filter by split")
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    args = parser.parse_args()

    with open('../config.json') as f:
        config = json.load(f)
    utils.init_logging()
    conn = utils.connect_db(config)
    individual_offense = IndividualOffenseETL(args.year, args.split, args.load, conn)
    individual_offense.run()
    conn.close()
