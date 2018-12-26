""" This module provides utility functions """
# Standard library imports
import logging
import sys
# Third party imports
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
# Local imports


def connect_db(config):
    """ Create database connection
    :param config: Dictionary with connection parameters
    :returns: Database connection object
    """
    if "port" not in config.keys():
        config["port"] = "5432"

    try:
        conn_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                    config["user"],
                    config["password"],
                    config["host"],
                    config["port"],
                    config["database"])
    except KeyError as e:
        print("Database connection parameter error")
        sys.exit(1)

    engine = create_engine(conn_str)
    try:
        conn = engine.connect()
    except SQLAlchemyError as e:
        print("Failed to connect to database")
        print(e)
        sys.exit(1)
    return conn


def db_load_data(data, table, conn, exit=False, **kwargs):
    """ Load DataFrame into database table """
    try:
        data.to_sql(table, conn, **kwargs)
    except Exception as e:
        print("Unable to load data into", table, "table")
        print(e)
        if exit:
            conn.close()
            sys.exit(1)
    else:
        print("Successfully loaded", len(data), "records into", table, "table")


def init_logging():
    """ Initialize logging """
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(message)s  <%(funcName)s %(module)s.py:%(lineno)d>',
                        datefmt='%H:%M:%S')
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
