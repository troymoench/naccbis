""" This module provides utility functions """
# Standard library imports
import logging
import os
from typing import List, Dict

# Third party imports
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError

# Local imports
import conf


# @event.listens_for(Engine, "connect")
# def my_on_connect(dbapi_con, connection_record):
#     print("New DBAPI connection:", dbapi_con.dsn)


@event.listens_for(Engine, "engine_connect")
def receive_engine_connect(conn, branch):
    logging.info("Successfully connected to database")
    logging.debug("DSN: %s", conn.connection.dsn)


# @event.listens_for(Engine, 'close')
# def receive_close(dbapi_connection, connection_record):
#     print("Closed connection")


# @event.listens_for(Engine, 'checkout')
# def receive_checkout(dbapi_connection, connection_record, connection_proxy):
#     print("Retrieving a connection from pool")


# @event.listens_for(Engine, 'checkin')
# def receive_checkin(dbapi_connection, connection_record):
#     print("Returning connection to pool")


# @event.listens_for(Engine, 'before_cursor_execute')
# def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     logging.debug("SQL statement: %s", statement)
#     logging.debug("SQL params: %s", parameters)


# @event.listens_for(Engine, 'handle_error')
# def receive_handle_error(exception_context):
#     print("error handler")
#     print(type(exception_context.sqlalchemy_exception))
#     print(exception_context.engine)
#     print(exception_context.connection)


def create_db_engine(config: Dict[str, str]) -> Engine:
    """Create database engine

    :param config: Dictionary with connection parameters
    :returns: Database engine object
    """
    try:
        conn_url = URL.create(**config)
    except TypeError:
        logging.error("Database connection parameter error")
        raise

    return create_engine(conn_url)


def connect_db(config: Dict[str, str]) -> Connection:
    """Create database connection

    :param config: Dictionary with connection parameters
    :returns: Database connection object
    """
    logging.info("Connecting to database")
    engine = create_db_engine(config)
    try:
        conn = engine.connect()
    except SQLAlchemyError:
        logging.error("Failed to connect to database %s", config.get("database"))
        raise
    return conn


def db_load_data(data: pd.DataFrame, table: str, conn: Connection, **kwargs) -> None:
    """Load DataFrame into database table"""
    try:
        data.to_sql(table, conn, **kwargs)
    except Exception as e:
        logging.error("Unable to load data into %s table", table)
        logging.error(e)
    else:
        logging.info("Successfully loaded %s records into %s table", len(data), table)


def init_config():
    """Initialize configuration"""
    config = {
        "DB": getattr(conf, "DB", None),
        "LOGGING": os.environ.get("LOG_LEVEL", "INFO"),
    }
    return config


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


def parse_year(year: str) -> List[int]:
    """Parse a string of year(s), e.g. 2017, 2015:2017

    :param year: The string representation of a year or range of years
    :returns: List of years (integers)
    """
    # if no colon exists, single year
    if ":" not in year:
        return [int(year)]
    else:
        temp = [int(yr) for yr in year.split(":")]
        temp.sort()  # ascending
        rng = list(range(temp[0], temp[1] + 1))
        # rng.sort(reverse=True)  # descending
        return rng


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
    return str(season - 1) + "-" + str(season - 2000)
