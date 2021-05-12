""" This script is the data cleaning controller """
# Standard library imports
import logging
from typing import List, Tuple

# Third party imports
import click

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
from naccbis.Common import utils


FINAL_PARSER_DESCRIPTION = """
Clean final stats.

\b
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

\b
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


@click.group(help=__doc__)
def cli():
    pass


def run_etls(
    etl_nums: List[int], year: int, splits: List[str], load_db: bool, conn: object
) -> None:
    """Run ETL's for a given year

    :param
    :returns:
    """
    etls = {
        1: IndividualOffenseETL,
        2: IndividualPitchingETL,
        3: TeamOffenseETL,
        4: TeamPitchingETL,
        6: LeagueOffenseETL,
        7: LeaguePitchingETL,
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


@cli.command(help=FINAL_PARSER_DESCRIPTION)
@click.argument("year", type=utils.parse_year)
@click.option(
    "-S",
    "--stat",
    type=click.IntRange(min=1, max=7),
    multiple=True,
    default=range(1, 8),
    help="Select ETL(s) to run. Provide list or omit argument for all ETLs",
)
@click.option(
    "-s",
    "--split",
    type=click.Choice(["overall", "conference", "all"]),
    default="all",
    show_default=True,
    help="Split choices",
)
@click.option("--load", is_flag=True, help="Load data into database")
@click.option(
    "-v", "--verbose", is_flag=True, help="Print extra information to standard out"
)
def final(
    year: List[int], stat: Tuple[int], split: str, load: bool, verbose: bool
) -> None:
    """Run ETLs for the final subcommand

    :param args: Arguments for the ETLs
    :param conn: Database connection object
    """
    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    logging.info("Initializing cleaning controller script")
    conn = utils.connect_db(config["DB"])

    if split == "all":
        splits = ["overall", "conference"]
    else:
        splits = [split]

    for year_ in year:
        logging.info("Running ETLs for %s", year_)
        run_etls(list(stat), year_, splits, load, conn)

    conn.close()
    logging.info("Cleaning completed")


# @cli.command(help=INSEASON_PARSER_DESCRIPTION)
# def inseason() -> None:
#     raise NotImplementedError("Inseason ETL is not supported yet")


if __name__ == "__main__":
    cli()  # pragma: no cover
