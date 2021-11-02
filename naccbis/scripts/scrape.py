""" This script is the scraping controller """
# Standard library imports
from datetime import date
import logging
from typing import List, Dict, Sequence, Type, Tuple, Union

# Third party imports
import click
from sqlalchemy.engine.base import Connection

# Local imports
from naccbis.scraping import (
    BaseScraper,
    GameLogScraper,
    IndividualOffenseScraper,
    IndividualPitchingScraper,
    TeamFieldingScraper,
    TeamOffenseScraper,
    TeamPitchingScraper,
)
from naccbis.Common import utils
from naccbis.Common.splits import GameLogSplit, Split
from naccbis.Common.settings import Settings


PARSER_EPILOG = """\b
Examples:
   scrape.py final 2015:2017
   scrape.py final 2017 -S 1,3 -s conference -o sql
   scrape.py inseason
   scrape.py inseason -S 6 -s overall -o csv
"""

FINAL_PARSER_DESCRIPTION = """
Scrape end of the year final stats.

\b
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

\b
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


@click.group(help=__doc__, epilog=PARSER_EPILOG)
def cli():
    pass


def run_scrapers(
    scraper_nums: List[int],
    year: str,
    splits: Sequence[Union[Split, GameLogSplit]],
    output: str,
    inseason: bool,
    verbose: bool,
    conn: Connection,
) -> None:
    """Run selected scrapers for a given year

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
        5: TeamFieldingScraper,
    }

    for split in splits:
        for num in scraper_nums:
            if num in scrapers.keys():
                runScraper = scrapers[num](
                    year, split, output, inseason, verbose, conn=conn
                )
                runScraper.info()
                runScraper.run()
                runScraper.export()

    # Game logs have special splits
    if 6 in scraper_nums:
        for split in list(GameLogSplit):
            gameLogScraper = GameLogScraper(
                year, split, output, inseason, verbose, conn=conn
            )
            gameLogScraper.info()
            gameLogScraper.run()
            gameLogScraper.export()


@cli.command(help=FINAL_PARSER_DESCRIPTION)
@click.argument("year", type=utils.parse_year)
@click.option(
    "-S",
    "--stat",
    type=click.IntRange(min=1, max=6),
    multiple=True,
    default=range(1, 7),
    help="Select stat scraper(s) to run. Provide list or omit argument for all scrapers",
)
@click.option(
    "-s",
    "--split",
    type=click.Choice(["overall", "conference", "all"]),
    default="all",
    show_default=True,
    help="Split choices",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["csv", "sql"]),
    default="csv",
    show_default=True,
    help="Output choices",
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Print extra information to standard out"
)
def final(
    year: List[int], stat: Tuple[int], split: str, output: str, verbose: bool
) -> None:
    """Scrape end of the year final stats

    :param args: Arguments for the scrapers
    """
    config = Settings(app_name="scrape")
    utils.init_logging(config.log_level)
    conn = utils.connect_db(config.get_db_url())

    logging.info("Initializing scraping controller script")
    years = [utils.season_to_year(x) for x in year]

    if split == "all":
        splits = list(Split)
    else:
        splits = [Split(split)]

    for year_ in years:
        print("\nScraping:", year_, "\n")

        run_scrapers(
            list(stat),
            year_,
            splits,
            output,
            inseason=False,
            verbose=verbose,
            conn=conn,
        )
    conn.close()
    logging.info("Scraping completed")


@cli.command(help=INSEASON_PARSER_DESCRIPTION)
@click.option(
    "-S",
    "--stat",
    type=click.IntRange(min=1, max=6),
    multiple=True,
    default=list(range(1, 7)),
    help="Select stat scraper(s) to run. Provide list or omit argument for all scrapers",
)
@click.option(
    "-s",
    "--split",
    type=click.Choice(["overall", "conference", "all"]),
    default="all",
    show_default=True,
    help="Split choices",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["csv", "sql"]),
    default="csv",
    show_default=True,
    help="Output choices",
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Print extra information to standard out"
)
def inseason(stat: Tuple[int], split: str, output: str, verbose: bool) -> None:
    """Run scrapers for the inseason subcommand

    :param args: Arguments for the scrapers
    """
    config = Settings(app_name="scrape")
    utils.init_logging(config.log_level)
    conn = utils.connect_db(config.get_db_url())

    logging.info("Initializing scraping controller script")
    season = date.today().year
    year = utils.season_to_year(season)

    if split == "all":
        splits = list(Split)
    else:
        splits = [Split(split)]

    run_scrapers(
        list(stat), year, splits, output, inseason=True, verbose=verbose, conn=conn
    )
    conn.close()
    logging.info("Scraping completed")


if __name__ == "__main__":
    cli()  # pragma: no cover
