""" This script is the data cleaning controller """
# Standard library imports
import argparse
import logging
import sys
# Third party imports
# Local imports
from CleanGameLogs import GameLogETL
from CleanIndividualOffense import IndividualOffenseETL
from CleanIndividualPitching import IndividualPitchingETL
from CleanTeamOffense import TeamOffenseETL
from CleanTeamPitching import TeamPitchingETL
from LeagueTotals import LeagueOffenseETL, LeaguePitchingETL
import Common.utils as utils


def run_etls(etl_nums, year, splits, load_db, conn):
    """ Run ETL's for a given year
    :param
    :returns:
    """
    etls = {1: IndividualOffenseETL,
            2: IndividualPitchingETL,
            3: TeamOffenseETL,
            4: TeamPitchingETL,
            6: LeagueOffenseETL,
            7: LeaguePitchingETL}

    for split in splits:
        for num in etl_nums:
            if num in etls.keys():
                etl = etls[num](year, split, load_db, conn)
                etl.run()

    # GameLogs don't have any splits
    if 5 in etl_nums:
        gameLogETL = GameLogETL(year, load_db, conn)
        gameLogETL.run()


def final(args, conn):
    years = utils.parse_year(args.year)

    # parse split
    if args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [args.split]

    accepted = list(range(1, 8))
    etls = utils.parse_stat(args.stat, accepted)

    if len(etls) == 0:
        print("Unrecognized stat option")
        final_parser.print_usage()
        sys.exit(1)

    for year in years:
        run_etls(etls, year, splits, args.load, conn)


def inseason(args):
    raise NotImplementedError("Inseason ETL is not supported yet")


def add_common_args(parser):
    """ Add common arguments to the parser
    :param parser: Parser object to add arguments to
    """
    # NOTE: These args are common to all subcommands. Unfortunately, they can't just
    # be added to the top level parser because the subcommand parser parses all
    # args after the subcommand.
    parser.add_argument("-s", "--split", type=str, choices=["overall", "conference", "all"],
                        default="overall", metavar="SPLIT", help="Filter by split")
    parser.add_argument("-S", "--stat", type=str, default="all", metavar="STAT",
                        help="Select ETL(s) to run. Provide comma separated list or all for multiple")

    parser.add_argument("--load", action="store_true",
                        help="Load data into database")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="NACCBIS Cleaning controller")
    subparsers = parser.add_subparsers()

    # parser for 'final' subcommand
    final_parser = subparsers.add_parser("final",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='Clean final stats\n\n'
                                         '     Stat Options\n'
                                         '  ---------------------\n'
                                         '  1) Individual Offense\n'
                                         '  2) Individual Pitching\n'
                                         '  3) Team Offense\n'
                                         '  4) Team Pitching\n'
                                         '  5) Game Logs\n'
                                         '  6) League Offense\n'
                                         '  7) League Pitching\n'
                                         '  all) All\n')

    final_parser.add_argument("year", type=str, help="A year or range of years")
    add_common_args(final_parser)
    # set the callback function for this subcommand
    final_parser.set_defaults(func=final)

    # parser for 'inseason' subcommand
    inseason_parser = subparsers.add_parser("inseason",
                                            formatter_class=argparse.RawDescriptionHelpFormatter,
                                            description='Clean stats during the season. '
                                            'A column is added for the scrape date.\n\n'
                                            '     Stat Options\n'
                                            '  ---------------------\n'
                                            '  1) Individual Offense\n'
                                            '  2) Individual Pitching\n'
                                            '  3) Team Offense\n'
                                            '  4) Team Pitching\n'
                                            '  5) Game Logs\n'
                                            '  6) League Offense\n'
                                            '  7) League Pitching\n'
                                            '  all) All\n')

    # set the callback function for this subcommand
    inseason_parser.set_defaults(func=inseason)

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])

    logging.info("Initializing cleaning controller script")
    logging.info("Command line args received: %s", sys.argv[1:])

    args = parser.parse_args()
    conn = utils.connect_db(config["DB"])
    args.func(args, conn)

    conn.close()
    logging.info("Cleaning completed")
