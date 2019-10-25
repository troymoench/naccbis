""" This script is the scraping controller """
# Standard library imports
import argparse
from datetime import date
import sys
import logging
# Third party imports
# Local imports
from naccbis.Scraping.ScrapeGameLog import GameLogScraper
from naccbis.Scraping.ScrapeIndividualOffense import IndividualOffenseScraper
from naccbis.Scraping.ScrapeIndividualPitching import IndividualPitchingScraper
from naccbis.Scraping.ScrapeTeamFielding import TeamFieldingScraper
from naccbis.Scraping.ScrapeTeamOffense import TeamOffenseScraper
from naccbis.Scraping.ScrapeTeamPitching import TeamPitchingScraper
import naccbis.Common.utils as utils


def run_scrapers(scraper_nums, year, splits, output, inseason, verbose):
    """ Run selected scrapers for a given year

    :param scraper_nums: List of integers that correspond to the scrapers to be run
    :param year: The integer representation of the year
    :param splits: List of splits
    :param output: Output type
    :param inseason: Scraping during the season?
    :param verbose: Print extra information to standard out?
    """
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


def final(args):
    """ Run scrapers for the final subcommand

    :param args: Arguments for the scrapers
    """
    # parse year
    seasons = utils.parse_year(args.year)
    years = [utils.season_to_year(x) for x in seasons]

    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    # parse stat
    accepted = list(range(1, 7))
    scrapers = utils.parse_stat(args.stat, accepted)
    if len(scrapers) == 0:
        print("Unrecognized stat option")
        final_parser.print_usage()
        sys.exit(1)

    for year in years:
        print("\nScraping:", year, "\n")

        run_scrapers(scrapers, year, splits, args.output, inseason=False, verbose=args.verbose)


def inseason(args):
    """ Run scrapers for the inseason subcommand

    :param args: Arguments for the scrapers
    """
    # current year
    year = date.today().year
    year = utils.season_to_year(year)

    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    # parse stat
    accepted = list(range(1, 7))
    scrapers = utils.parse_stat(args.stat, accepted)
    if len(scrapers) == 0:
        print("Unrecognized stat option")
        inseason_parser.print_usage()
        sys.exit(1)

    run_scrapers(scrapers, year, splits, args.output, inseason=True, verbose=args.verbose)


def add_common_args(parser):
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
    parser.add_argument("-S", "--stat", type=str, default="all", metavar="STAT",
                        help="Select stat scraper(s) to run. Provide comma separated list or all for multiple")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__,
                                     epilog="examples:\n"
                                            "   scrape.py final 2015:2017\n"
                                            "   scrape.py final 2017 -S 1,3 -s conference -o sql\n"
                                            "   scrape.py inseason\n"
                                            "   scrape.py inseason -S 6 -s overall -o csv")
    subparsers = parser.add_subparsers()

    final_parser = subparsers.add_parser("final",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='Scrape end of the year final stats\n\n'
                                         '     Stat Options\n'
                                         '  ---------------------\n'
                                         '  1) Individual Offense\n'
                                         '  2) Individual Pitching\n'
                                         '  3) Team Offense\n'
                                         '  4) Team Pitching\n'
                                         '  5) Team Fielding\n'
                                         '  6) Game Logs\n'
                                         '  all) All\n')

    final_parser.add_argument("year", type=str, help="A year or range of years")
    add_common_args(final_parser)
    final_parser.set_defaults(func=final)

    inseason_parser = subparsers.add_parser("inseason",
                                            formatter_class=argparse.RawDescriptionHelpFormatter,
                                            description='Scrape stats during the season. '
                                            'A column is added for the scrape date.\n\n'
                                            '     Stat Options\n'
                                            '  ---------------------\n'
                                            '  1) Individual Offense\n'
                                            '  2) Individual Pitching\n'
                                            '  3) Team Offense\n'
                                            '  4) Team Pitching\n'
                                            '  5) Team Fielding\n'
                                            '  6) Game Logs\n'
                                            '  all) All\n')
    add_common_args(inseason_parser)
    inseason_parser.set_defaults(func=inseason)

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])

    args = parser.parse_args()
    logging.info("Initializing scraping controller script")
    logging.info("Command line args received: %s", sys.argv[1:])
    args.func(args)

    logging.info("Scraping completed")