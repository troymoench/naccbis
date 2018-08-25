import sys
import argparse
import pandas as pd
import logging
import config
from datetime import date
import ScrapeFunctions as sf
from ScrapeGameLog import GameLogScraper
from ScrapeIndividualOffense import IndividualOffenseScraper
from ScrapeIndividualPitching import IndividualPitchingScraper
from ScrapeTeamFielding import TeamFieldingScraper
from ScrapeTeamOffense import TeamOffenseScraper
from ScrapeTeamPitching import TeamPitchingScraper


# This script is the scraping controller
# TODO: fix csv output: combine files? zip?


def parse_year(year):
    # parses a string of year(s), e.g. 2017, 2015:2017
    # if no colon exists, single year
    if ':' not in year:
        return [int(year)]
    else:
        temp = [int(yr) for yr in year.split(':')]
        temp.sort()  # ascending
        rng = list(range(temp[0], temp[1]+1))
        # rng.sort(reverse=True)  # descending
        return rng


def parse_stat(stats, accepted_values):
    # parses a string of stat(s), e.g. 1,2 all
    if stats == "all":
        return accepted_values
    else:
        temp = stats.replace(" ", "")
        temp = [int(stat) for stat in stats.split(',')]
        if set(temp).issubset(set(accepted_values)):
            temp.sort()  # ascending
            return temp
        else:
            return list()  # should raise an exception


def run_scrapers(scraper_nums, year, splits, output, inseason, verbose):
    # run selected scrapers for a given year
    scrapers = {1: IndividualOffenseScraper,
                2: IndividualPitchingScraper,
                3: TeamOffenseScraper,
                4: TeamPitchingScraper,
                5: TeamFieldingScraper}

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


def final():
    final_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                           description='Scrape end of the year final stats\n\n'
                                           '     Stat Options\n'
                                           '  ---------------------\n'
                                           '  1) Individual Offense\n'
                                           '  2) Individual Pitching\n'
                                           '  3) Team Offense\n'
                                           '  4) Team Pitching\n'
                                           '  5) Team Fielding\n'
                                           '  6) Game Logs\n'
                                           '  all) All\n',
                                           usage="%(prog)s final YEAR [-h] [-s SPLIT] [-S STAT] [-o OUTPUT] [-v]")
    final_parser.add_argument("year", type=str, help="A year or range of years")
    final_parser.add_argument("-s", "--split", type=str, choices=["overall", "conference", "all"],
                              default="all", metavar="SPLIT", help="Split choices: overall, conference, all (default)")
    final_parser.add_argument("-S", "--stat", type=str, default="all", metavar="STAT",
                              help="Select stat scraper(s) to run. Provide comma separated list or all for multiple")

    final_parser.add_argument("-o", "--output", type=str, choices=["csv", "sql"],
                              default="csv", metavar="OUTPUT", help="Output choices: csv (default), sql")
    final_parser.add_argument("-v", "--verbose", action="store_true", help="Print extra information to standard out")

    final_args = final_parser.parse_args(sys.argv[2:])
    # print(final_args.year)

    # parse year
    seasons = parse_year(final_args.year)
    # print(seasons)
    years = [sf.season_to_year(x) for x in seasons]
    # print(years)

    # print(final_args.split)

    # parse split
    if final_args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [final_args.split]
    # print(splits)

    # parse stat
    accepted = list(range(1, 7))
    scrapers = parse_stat(final_args.stat, accepted)
    # print(scrapers)
    if len(scrapers) == 0:
        print("Unrecognized stat option")
        final_parser.print_usage()
        exit(1)

    # parse output
    output = final_args.output
    # print(output)

    # parse verbose
    verbose = final_args.verbose
    # if verbose:
    #     print("Verbose")

    for year in years:
        print("\nScraping:", year, "\n")

        run_scrapers(scrapers, year, splits, output, inseason=False, verbose=verbose)


def inseason():
    inseason_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
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
                                              '  all) All\n',
                                              usage="%(prog)s inseason [-h] [-s SPLIT] [-S STAT] [-o OUTPUT] [-v]")
    inseason_parser.add_argument("-s", "--split", type=str, choices=["overall", "conference", "all"],
                                 default="all", metavar="SPLIT",
                                 help="Split choices: overall, conference, all (default)")
    inseason_parser.add_argument("-S", "--stat", type=str, default="all", metavar="STAT",
                                 help="Select stat scraper(s) to run. Provide comma separated list or all for multiple")

    inseason_parser.add_argument("-o", "--output", type=str, choices=["csv", "sql"],
                                 default="csv", metavar="OUTPUT", help="Output choices: csv (default), sql")
    inseason_parser.add_argument("-v", "--verbose", action="store_true", help="Print extra information to standard out")

    inseason_args = inseason_parser.parse_args(sys.argv[2:])
    # print(inseason_args)

    # current year
    year = date.today().year
    year = sf.season_to_year(year)
    # print(year)

    # parse split
    if inseason_args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [inseason_args.split]
    # print(splits)

    # parse stat
    accepted = list(range(1, 7))
    scrapers = parse_stat(inseason_args.stat, accepted)
    # print(scrapers)
    if len(scrapers) == 0:
        print("Unrecognized stat option")
        inseason_parser.print_usage()
        exit(1)

    # parse output
    output = inseason_args.output
    # print(output)

    # parse verbose
    verbose = inseason_args.verbose
    # if verbose:
    #     print("Verbose")

    run_scrapers(scrapers, year, splits, output, inseason=True, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This script is the NACCBIS scraping controller",
                                     epilog="examples:\n"
                                            "   scrape.py final 2015:2017\n"
                                            "   scrape.py final 2017 -S 1,3 -s conference -o sql\n"
                                            "   scrape.py inseason\n"
                                            "   scrape.py inseason -S 6 -s overall -o csv")
    parser.add_argument("type", help="Select the type of stats to scrape", choices=["final", "inseason"])
    args = parser.parse_args(sys.argv[1:2])

    # log that the script has started
    logging.info("Initializing scraping controller script")
    logging.info("Command line args received: %s", sys.argv[1:])

    if args.type == "final":
        final()
    elif args.type == "inseason":
        inseason()
    else:
        print("This can't happen")

    logging.info("Scraping completed")
