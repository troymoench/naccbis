""" This script is the scraping controller """
# Standard library imports
import argparse
from datetime import date
import sys
import logging
from typing import List, Dict, Type, Optional
# Third party imports
# Local imports
from naccbis.Scraping import (
    BaseScraper,
    GameLogScraper,
    IndividualOffenseScraper,
    IndividualPitchingScraper,
    TeamFieldingScraper,
    TeamOffenseScraper,
    TeamPitchingScraper,
)
import naccbis.Common.utils as utils
from naccbis import __version__


PARSER_EPILOG = """
examples:
   scrape.py final 2015:2017
   scrape.py final 2017 -S 1,3 -s conference -o sql
   scrape.py inseason
   scrape.py inseason -S 6 -s overall -o csv
"""

FINAL_PARSER_DESCRIPTION = """
Scrape end of the year final stats

     Stat Options
  ---------------------
  1) Individual Offense
  2) Individual Pitching
  3) Team Offense
  4) Team Pitching
  5) Team Fielding
  6) Game Logs
  all) All
"""

INSEASON_PARSER_DESCRIPTION = """
Scrape stats during the season.
A column is added for the scrape date.

     Stat Options
  ---------------------
  1) Individual Offense
  2) Individual Pitching
  3) Team Offense
  4) Team Pitching
  5) Team Fielding
  6) Game Logs
  all) All
"""


def run_scrapers(scraper_nums: List[int], year: str, splits: List[str],
                 output: str, inseason: bool, verbose: bool) -> None:
    """ Run selected scrapers for a given year

    :param scraper_nums: List of integers that correspond to the scrapers to be run
    :param year: The integer representation of the year
    :param splits: List of splits
    :param output: Output type
    :param inseason: Scraping during the season?
    :param verbose: Print extra information to standard out?
    """
    scrapers: Dict[int, Type[BaseScraper]]
    scrapers = {
        1: IndividualOffenseScraper,
        2: IndividualPitchingScraper,
        3: TeamOffenseScraper,
        4: TeamPitchingScraper,
        5: TeamFieldingScraper
    }

    for split in splits:
        for num in scraper_nums:
            if num in scrapers.keys():
                runScraper = scrapers[num](year, split, output, inseason, verbose)
                runScraper.info()
                runScraper.run()
                runScraper.export()

    if 6 in scraper_nums:
        for split in ["hitting", "pitching", "fielding"]:
            gameLogScraper = GameLogScraper(year, split, output, inseason, verbose)
            gameLogScraper.info()
            gameLogScraper.run()
            gameLogScraper.export()


def final(args) -> None:
    """ Run scrapers for the final subcommand

    :param args: Arguments for the scrapers
    """
    years = [utils.season_to_year(x) for x in args.year]

    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    for year in years:
        print("\nScraping:", year, "\n")

        run_scrapers(args.stat, year, splits, args.output, inseason=False, verbose=args.verbose)


def inseason(args) -> None:
    """ Run scrapers for the inseason subcommand

    :param args: Arguments for the scrapers
    """
    # current year
    season = date.today().year
    year = utils.season_to_year(season)

    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    run_scrapers(args.stat, year, splits, args.output, inseason=True, verbose=args.verbose)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """ Add common arguments to the parser

    :param parser: Parser object to add arguments to
    """
    # NOTE: These args are common to all subcommands. Unfortunately, they can't just
    # be added to the top level parser because the subcommand parser parses all
    # args after the subcommand.

    parser.add_argument("-o", "--output", type=str, choices=["csv", "sql"],
                        default="csv", metavar="OUTPUT", help="Output choices: csv (default), sql")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print extra information to standard out")
    parser.add_argument("-s", "--split", type=str, choices=["overall", "conference", "all"],
                        default="all", metavar="SPLIT",
                        help="Split choices: overall, conference, all (default)")
    parser.add_argument("-S", "--stat", type=int, nargs="*", choices=range(1, 7),
                        default=range(1, 7), metavar="STAT",
                        help="Select stat scraper(s) to run. "
                             "Provide list or omit argument for all scrapers")


def parse_args(args: Optional[List[str]]) -> argparse.Namespace:
    """ Build parser object and parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__,
                                     epilog=PARSER_EPILOG)
    parser.add_argument("--version", action="version", version="naccbis {}".format(__version__))
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
    logging.info("Initializing scraping controller script")
    logging.info("Command line args received: %s", raw_args)
    args.func(args)

    logging.info("Scraping completed")


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
