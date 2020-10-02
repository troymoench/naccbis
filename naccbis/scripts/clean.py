""" This script is the data cleaning controller """
# Standard library imports
import argparse
import logging
import sys
from typing import List, Optional
# Third party imports
# Local imports
from naccbis.Cleaning import (
    GameLogETL,
    IndividualOffenseETL,
    IndividualPitchingETL,
    TeamOffenseETL,
    TeamPitchingETL,
    LeagueOffenseETL,
    LeaguePitchingETL,
)
import naccbis.Common.utils as utils

FINAL_PARSER_DESCRIPTION = """
Clean final stats

     Stat Options
  ---------------------
  1) Individual Offense
  2) Individual Pitching
  3) Team Offense
  4) Team Pitching
  5) Game Logs
  6) League Offense
  7) League Pitching
  all) All
"""

INSEASON_PARSER_DESCRIPTION = """
Clean stats during the season.
A column is added for the scrape date.

     Stat Options
  ---------------------
  1) Individual Offense
  2) Individual Pitching
  3) Team Offense
  4) Team Pitching
  5) Game Logs
  6) League Offense
  7) League Pitching
  all) All
"""


def run_etls(etl_nums: List[int], year: str, splits: List[str],
             load_db: bool, conn: object) -> None:
    """ Run ETL's for a given year

    :param
    :returns:
    """
    etls = {
        1: IndividualOffenseETL,
        2: IndividualPitchingETL,
        3: TeamOffenseETL,
        4: TeamPitchingETL,
        6: LeagueOffenseETL,
        7: LeaguePitchingETL
    }

    for split in splits:
        for num in etl_nums:
            if num in etls.keys():
                etl = etls[num](year, split, load_db, conn)
                etl.run()

    # GameLogs don't have any splits
    if 5 in etl_nums:
        gameLogETL = GameLogETL(year, load_db, conn)
        gameLogETL.run()


def final(args, conn: object) -> None:
    """ Run ETLs for the final subcommand

    :param args: Arguments for the ETLs
    :param conn: Database connection object
    """
    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    for year in args.year:
        logging.info("Running ETLs for %s", year)
        run_etls(args.stat, year, splits, args.load, conn)


def inseason(args, conn: object) -> None:
    raise NotImplementedError("Inseason ETL is not supported yet")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """ Add common arguments to the parser

    :param parser: Parser object to add arguments to
    """
    # NOTE: These args are common to all subcommands. Unfortunately, they can't just
    # be added to the top level parser because the subcommand parser parses all
    # args after the subcommand.
    parser.add_argument("-s", "--split", type=str, choices=["overall", "conference", "all"],
                        default="all", metavar="SPLIT", help="Filter by split")
    parser.add_argument("-S", "--stat", type=int, nargs="*", choices=range(1, 8),
                        default=range(1, 8), metavar="STAT",
                        help="Select ETL(s) to run. "
                             "Provide list or omit argument for all ETLs")

    parser.add_argument("--load", action="store_true",
                        help="Load data into database")


def parse_args(args: Optional[List[str]]) -> argparse.Namespace:
    """ Build parser object and parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="NACCBIS Cleaning controller")
    subparsers = parser.add_subparsers()

    final_parser = subparsers.add_parser("final",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=FINAL_PARSER_DESCRIPTION)

    final_parser.add_argument("year", type=utils.parse_year, help="A year or range of years")
    add_common_args(final_parser)
    final_parser.set_defaults(func=final)

    inseason_parser = subparsers.add_parser("inseason",
                                            formatter_class=argparse.RawDescriptionHelpFormatter,
                                            description=INSEASON_PARSER_DESCRIPTION)
    add_common_args(inseason_parser)
    inseason_parser.set_defaults(func=inseason)
    return parser.parse_args(args)


def main(raw_args: Optional[List[str]] = sys.argv[1:]) -> None:
    """ Script entry point """
    config = utils.init_config()
    utils.init_logging(config["LOGGING"])

    args = parse_args(raw_args)
    logging.info("Initializing cleaning controller script")
    logging.info("Command line args received: %s", raw_args)
    conn = utils.connect_db(config["DB"])
    args.func(args, conn)

    conn.close()
    logging.info("Cleaning completed")


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
