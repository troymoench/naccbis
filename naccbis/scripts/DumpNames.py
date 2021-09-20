"""This script used to identify inconsistencies with player names.
These inconsistencies include, but are not limited to:
1. Typos
2. Name changes
3. Nicknames
"""
# Standard library imports
from pathlib import Path

# Third party imports
import click
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection

# Local imports
from naccbis.Cleaning import CleanFunctions
from naccbis.Common import utils
from naccbis.Common.settings import Settings


def load_temp_table(conn: Connection, data: pd.DataFrame) -> None:
    sql = """
    CREATE TEMP TABLE dump_names_temp (
        lname text, fname text, team text, season integer, pos text
    )
    """
    conn.execute(sql)
    utils.db_load_data(data, "dump_names_temp", conn, if_exists="append", index=False)


def levenshtein_analysis(
    conn: Connection, lev_first: int, lev_last: int
) -> pd.DataFrame:
    """Perform a Levenshtein analysis on first names and last names.
    This is used for identifying typos.

    :param conn: Database connection
    :param lev_first: Levenshtein distance between first names
    :param lev_last: Levenshtein distance between last names
    :returns: A DataFrame with player-season pairs that meet the filter parameters
    """

    if lev_last > 0:
        lname_condition = "levenshtein(t1.lname, t2.lname) = :lev_last"
    else:
        lname_condition = "t1.lname = t2.lname"

    if lev_first > 0:
        fname_condition = "levenshtein(t1.fname, t2.fname) = :lev_first"
    else:
        fname_condition = "t1.fname = t2.fname"

    sql = f"""
    select
        t1.lname as lname1, t1.fname as fname1, t1.team as team1, t1.season as season1, t1.pos as pos1,
        t2.lname as lname2, t2.fname as fname2, t2.team as team2, t2.season as season2, t2.pos as pos2
    from dump_names_temp t1
    join dump_names_temp t2
    on {lname_condition}
    and {fname_condition}
    order by t1.lname, t1.fname, t1.season, t2.lname, t2.fname, t2.season;
    """
    params = {"lev_last": lev_last, "lev_first": lev_first}

    return pd.read_sql_query(text(sql), conn, params=params)


def nickname_analysis(conn: Connection) -> pd.DataFrame:
    """Perform a nickname analysis on first names.
    This is used for identifying inconsistencies due to nicknames.

    :param conn: Database connection
    :returns: A DataFrame with player-season pairs with a matching name and
              nickname in the lookup table.
    """

    sql = """
    select
        t1.lname as lname,
        t1.fname as fname1, t1.team as team1, t1.season as season1,
        t2.fname as fname2, t2.team as team2, t2.season as season2
    from dump_names_temp t1
    join dump_names_temp t2
    on t1.lname = t2.lname
    and t1.fname != t2.fname
    join nicknames n
    on t1.fname = n.name
    and t2.fname = n.nickname
    order by lname, fname1;
    """
    return pd.read_sql_query(text(sql), conn)


def duplicate_names_analysis(conn: Connection) -> pd.DataFrame:
    """Perform duplicate names analysis. Used for identifying transfers.

    :param conn: Database connection
    :returns: A DataFrame with player-seasons that have the same name but
              different teams.
    """

    sql = """
    select distinct
        t1.fname, t1.lname, t1.team, t1.season
    from dump_names_temp t1
    join dump_names_temp t2
    on t1.fname = t2.fname
    and t1.lname = t2.lname
    and t1.team != t2.team
    order by t1.lname, t1.fname, t1.team, t1.season;

    """
    return pd.read_sql_query(text(sql), conn)


@click.command(help="Identify inconsistencies with player names")
@click.option(
    "-c", "--corrections", is_flag=True, help="Apply existing name corrections"
)
@click.option(
    "-f",
    "--fname",
    "levenshtein_first",
    type=int,
    default=0,
    show_default=True,
    help="Filter first names by a Levenshtein distance",
)
@click.option(
    "-l",
    "--lname",
    "levenshtein_last",
    type=int,
    default=0,
    show_default=True,
    help="Filter last names by a Levenshtein distance",
)
@click.option("--nicknames", is_flag=True, help="Perform a nickname analysis")
@click.option("--duplicates", is_flag=True, help="Perform duplicate names analysis")
@click.option(
    "--dir",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    show_default=True,
    help="Directory to save the output to",
)
def cli(
    corrections: bool,
    levenshtein_first: int,
    levenshtein_last: int,
    nicknames: bool,
    duplicates: bool,
    dir: Path,
) -> None:
    """Script entry point"""

    config = Settings(app_name="dump-names")
    utils.init_logging(config.log_level)
    conn = utils.connect_db(config.get_db_url())

    batters = pd.read_sql_table("raw_batters_overall", conn)
    pitchers = pd.read_sql_table("raw_pitchers_overall", conn)
    if corrections:
        corrections_df = pd.read_sql_table("name_corrections", conn)

    batters = CleanFunctions.normalize_names(batters)
    pitchers = CleanFunctions.normalize_names(pitchers)

    batters = batters[["lname", "fname", "team", "season", "pos"]]
    pitchers = pitchers[["lname", "fname", "team", "season", "pos"]]

    data = pd.concat([batters, pitchers], ignore_index=True)
    data = data.sort_values(by=["lname", "fname", "team", "season"])

    if corrections:
        data = CleanFunctions.apply_corrections(data, corrections_df)
        data = data.sort_values(by=["lname", "fname", "team", "season"])

    load_temp_table(conn, data)

    if levenshtein_last or levenshtein_first:
        print("Performing levenshtein analysis")
        output = levenshtein_analysis(conn, levenshtein_first, levenshtein_last)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = dir / "levenshtein_analysis.csv"
            output.to_csv(filename, index=False)

    if nicknames:
        print("Performing nickname analysis")
        output = nickname_analysis(conn)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = dir / "nickname_analysis.csv"
            output.to_csv(filename, index=False)

    if duplicates:
        print("Performing duplicate names analysis")
        output = duplicate_names_analysis(conn)
        print("Found", len(output), "candidates")
        if len(output) > 0:
            print("Dumping to csv")
            filename = dir / "duplicate_names_analysis.csv"
            output.to_csv(filename, index=False)

    print("Dumping all names to csv")
    filename = dir / "all_names.csv"
    data.to_csv(filename, index=False)
    conn.close()


if __name__ == "__main__":
    cli()  # pragma: no cover
