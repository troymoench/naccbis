""" This script is used to verify data integrity in the database """
import click
import pandas as pd

from naccbis.common import utils
from naccbis.common.settings import Settings


def get_all_table_names(conn):
    """Fetch all of the table names from the database"""
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
    """
    return pd.read_sql_query(query, conn)["table_name"]


def table_count(conn, table):
    """Count the number of records in a given table"""
    query = f"SELECT count(*) FROM {table}"
    count = pd.read_sql_query(query, conn)
    count["table"] = table
    return count


@click.command(help=__doc__)
def cli():
    config = Settings(app_name="verify")
    conn = utils.connect_db(config.get_db_url())

    tables = get_all_table_names(conn)
    data = pd.concat([table_count(conn, table) for table in tables])
    data.sort_values("table", inplace=True)
    data.reset_index(drop=True, inplace=True)
    raw = data[data["table"].str.startswith("raw")]
    clean = data[~data["table"].str.startswith("raw")]
    print("***** Raw ******")
    print(raw[~raw["table"].str.endswith("inseason")])
    print(raw[raw["table"].str.endswith("inseason")])
    print("**** Clean *****")
    print(clean[~clean["table"].str.endswith("inseason")])
    print(clean[clean["table"].str.endswith("inseason")])
    conn.close()


if __name__ == "__main__":
    cli()
