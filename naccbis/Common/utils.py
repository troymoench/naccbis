""" This module provides utility functions """
# Standard library imports
import logging
import sys
# Third party imports
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
# Local imports
import naccbis.Common.conf as conf


def connect_db(config):
    """ Create database connection
    :param config: Dictionary with connection parameters
    :returns: Database connection object
    """
    logging.info("Connecting to database")

    try:
        conn_url = URL(**config)
    except TypeError:
        logging.error("Database connection parameter error")
        raise

    engine = create_engine(conn_url)
    try:
        conn = engine.connect()
    except SQLAlchemyError:
        logging.error("Failed to connect to database %s", config.get("database"))
        raise
    else:
        logging.info("Successfully connected to database %s", config.get("database"))
        logging.debug("DB Name: %s", config.get("database"))
        logging.debug("DB Host: %s", config.get("host"))
        logging.debug("DB Port: %s", config.get("port"))
        logging.debug("DB User: %s", config.get("username"))
    return conn


def db_load_data(data, table, conn, exit=False, **kwargs):
    """ Load DataFrame into database table """
    try:
        data.to_sql(table, conn, **kwargs)
    except Exception as e:
        logging.error("Unable to load data into %s table", table)
        logging.error(e)
        if exit:
            conn.close()
            sys.exit(1)
    else:
        logging.info("Successfully loaded %s records into %s table", len(data), table)


def init_config():
    """ Initialize configuration """
    config = {
        "DB": conf.DB,
        "LOGGING": conf.LOGGING
    }
    return config


def init_logging(config):
    """ Initialize logging """
    logging.basicConfig(level=config["level"],
                        format=config["format"],
                        datefmt=config["datefmt"])
    logging.getLogger('sqlalchemy.engine').setLevel("WARNING")


def parse_year(year):
    """ Parse a string of year(s), e.g. 2017, 2015:2017
    :param year: The string representation of a year or range of years
    :returns: List of years (integers)
    """
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
    """ Parse a string of stat options, e.g. 1,2 all
    :param stats: String of stat options to parse
    :param accepted_values: List of accepted stat options
    :returns: List of stat options (integers)
    """
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


def year_to_season(yr):
    """ Converts a school year into a season
    e.g. year_to_season("2016-17") returns 2017

    :param yr: String
    :returns: Int
    """
    return int(yr[0:4]) + 1


def season_to_year(season):
    """ Converts a season into a school year
    e.g. season_to_year(2017) returns "2016-17"

    :param season: Int
    :returns: String
    """
    return str(season - 1) + '-' + str(season - 2000)
