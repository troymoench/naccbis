""" This module provides utility functions """
# Standard library imports
import logging
from typing import Union, Any

# Third party imports
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError


@event.listens_for(Engine, "engine_connect")
def receive_engine_connect(conn, branch):
    logging.info("Successfully connected to database")
    logging.debug("DSN: %s", conn.connection.dsn)


def connect_db(db_url: Union[str, URL]) -> Connection:
    """Create database connection

    :param db_url: URL with connection parameters
    :returns: Database connection object
    """
    logging.info("Connecting to database")
    engine = create_engine(db_url)
    try:
        conn = engine.connect()
    except SQLAlchemyError as e:  # pragma: no cover
        logging.error("Failed to connect to database: %s", e)
        raise
    return conn


def db_load_data(
    data: pd.DataFrame, table: str, conn: Connection, **kwargs: Any
) -> None:
    """Load DataFrame into database table"""
    try:
        data.to_sql(table, conn, **kwargs)
    except Exception as e:  # pragma: no cover
        logging.error("Unable to load data into %s table", table)
        logging.error(e)
    else:
        logging.info(f"Successfully loaded {len(data)} records into {table} table")


def init_logging(level: str) -> None:
    """Initialize logging"""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s <%(name)s>",
        datefmt="%H:%M:%S",
    )
    # TODO: Dynamically configure additional loggers
    logging.getLogger("sqlalchemy.engine").setLevel("WARNING")
    logging.getLogger("sqlalchemy.pool").setLevel("INFO")


def parse_year(year: str) -> list[int]:
    """Parse a string of year(s), e.g. 2017, 2015:2017

    :param year: The string representation of a year or range of years
    :returns: List of years (integers)
    """
    if ":" not in year:
        return [int(year)]
    else:
        temp = [int(yr) for yr in year.split(":")]
        temp.sort()  # ascending
        start_year, end_year = temp
        return list(range(start_year, end_year + 1))


def year_to_season(yr: str) -> int:
    """Converts a school year into a season
    e.g. year_to_season("2016-17") returns 2017

    :param yr: String
    :returns: Int
    """
    return int(yr[0:4]) + 1


def season_to_year(season: int) -> str:
    """Converts a season into a school year
    e.g. season_to_year(2017) returns "2016-17"

    :param season: Int
    :returns: String
    """
    return f"{season - 1}-{season - 2000}"
