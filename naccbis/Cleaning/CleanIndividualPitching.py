""" Extract, Transform, Load Individual Pitching data

This script is used to clean individual pitching data and load into database
"""
# Standard library imports
import argparse
import logging
import os
# Third party imports
import numpy as np
import pandas as pd
# Local imports
from . import CleanFunctions
from naccbis.Common import (utils, metrics)


class IndividualPitchingETL:
    """ ETL class for individual pitching """
    VALID_SPLITS = ["overall", "conference"]
    CSV_DIR = "csv/"

    def __init__(self, year: int, split: str, load_db: bool, conn: object,
                 inseason: bool = False) -> None:
        self.year = year
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.load_db = load_db
        self.conn = conn
        self.inseason = inseason
        self.data: pd.DataFrame
        self.corrections: pd.DataFrame

    def extract(self) -> None:
        table = "raw_pitchers_{}".format(self.split)
        if self.inseason:
            table += "_inseason"
        logging.info("Reading data from %s", table)
        self.data = pd.read_sql_table(table, self.conn)
        logging.info("Read %s records from %s", len(self.data), table)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]
        self.corrections = pd.read_sql_table("name_corrections", self.conn)

    def transform(self) -> None:
        self.data = CleanFunctions.normalize_names(self.data)
        self.data = CleanFunctions.apply_corrections(self.data, self.corrections)
        self.data.drop(columns=["name"], inplace=True)

        self.data["ip"] = self.data["ip"].apply(CleanFunctions.convert_ip)
        conference = (self.split == "conference")
        self.data = metrics.basic_pitching_metrics(self.data, conference=conference)
        self.data.replace(pd.np.inf, np.nan, inplace=True)
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

        if self.inseason:
            columns.insert(5, "date")
        self.data = self.data[columns]

    def load(self) -> None:
        table = "pitchers_{}".format(self.split)
        if self.inseason:
            table += "_inseason"
        if self.load_db:
            logging.info("Loading data into database")
            utils.db_load_data(self.data, table, self.conn, if_exists="append", index=False)
        else:
            filename = table + ".csv"
            logging.info("Dumping to csv")
            self.data.to_csv(os.path.join(self.CSV_DIR, filename), index=False)

    def run(self) -> None:
        logging.info("Running %s", type(self).__name__)
        logging.info("Year: %s Split: %s Load: %s", self.year, self.split, self.load_db)
        self.extract()
        self.transform()
        self.load()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("--year", type=int, default=None, help="Filter by year")
    parser.add_argument("--split", type=str, default="overall", help="Filter by split")
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    args = parser.parse_args()

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])
    individual_pitching = IndividualPitchingETL(args.year, args.split, args.load,
                                                conn, inseason=True)
    individual_pitching.run()
    conn.close()
