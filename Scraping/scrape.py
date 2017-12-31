import sys
import argparse
import pandas as pd
import ScrapeFunctions as sf
from ScrapeGameLog import GameLogScraper
from ScrapeIndividualOffense import IndividualOffenseScraper
from ScrapeIndividualPitching import IndividualPitchingScraper
from ScrapeTeamFielding import TeamFieldingScraper
from ScrapeTeamOffense import TeamOffenseScraper
from ScrapeTeamPitching import TeamPitchingScraper


# This script is the scraping controller
# TODO: Unify standard output for default and verbose


def parse_year(year):
    # parses a string of year(s), e.g. 2017, 2015:2017
    # if no colon exists, single year
    if ':' not in year:
        return [int(year)]
    else:
        temp = [int(yr) for yr in year.split(':')]
        temp.sort()  # ascending
        rng = list(range(temp[0], temp[1]+1))
        rng.sort(reverse=True)  # descending
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
                                           '  all) All\n')
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
    print(years)

    # print(final_args.split)

    # parse split
    if final_args.split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [final_args.split]
    print(splits)

    # parse stat
    accepted = list(range(1, 7))
    scrapers = parse_stat(final_args.stat, accepted)
    print(scrapers)
    if len(scrapers) == 0:
        print("Unrecognized stat option")
        final_parser.print_usage()
        exit(1)

    # parse output
    output = final_args.output
    print(output)

    # parse verbose
    verbose = final_args.verbose
    if verbose:
        print("Verbose")

    for year in years:
        print("\nScraping:", year, "\n")

        for split in splits:
            if 1 in scrapers:
                indOffScraper = IndividualOffenseScraper(year, split, output, verbose=verbose)
                # indOffScraper.info()
                indOffScraper.run()
                indOffScraper.export()
            if 2 in scrapers:
                indPitScraper = IndividualPitchingScraper(year, split, output, verbose=verbose)
                # indPitScraper.info()
                indPitScraper.run()
                indPitScraper.export()
            if 3 in scrapers:
                teamOffScraper = TeamOffenseScraper(year, split, output, verbose=verbose)
                # teamOffScraper.info()
                teamOffScraper.run()
                teamOffScraper.export()
            if 4 in scrapers:
                teamPitScraper = TeamPitchingScraper(year, split, output, verbose=verbose)
                # teamPitScraper.info()
                teamPitScraper.run()
                teamPitScraper.export()
            if 5 in scrapers:
                teamFieldScraper = TeamFieldingScraper(year, split, output, verbose=verbose)
                # teamFieldScraper.info()
                teamFieldScraper.run()
                teamFieldScraper.export()

        if 6 in scrapers:
            gameLogScraper = GameLogScraper(year, "hitting", output, verbose=verbose)
            # gameLogScraper.info()
            gameLogScraper.run()
            gameLogScraper.export()
            gameLogScraper = GameLogScraper(year, "pitching", output, verbose=verbose)
            # gameLogScraper.info()
            gameLogScraper.run()
            gameLogScraper.export()
            gameLogScraper = GameLogScraper(year, "fielding", output, verbose=verbose)
            # gameLogScraper.info()
            gameLogScraper.run()
            gameLogScraper.export()


def inseason():
    print("Scrape inseason stats")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script is the NACCBIS scraping controller", epilog="examples:  scrape.py final 2015:2017")
    parser.add_argument("type", help="Select the type of stats to scrape", choices=["final", "inseason"])
    args = parser.parse_args(sys.argv[1:2])

    if args.type == "final":
        final()
    elif args.type == "inseason":
        inseason()
    else:
        print("This can't happen")

