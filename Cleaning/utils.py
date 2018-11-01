""" This module provides utility functions """
# Standard library imports
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
