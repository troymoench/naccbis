from typing import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, make_url

from naccbis.common.settings import Settings

NACCBIS_DB_URL = "postgresql:///naccbisdb_test"
SCHEMA_FILE = "db/schema_dump_2021_09_14.sql"


@pytest.fixture(scope="session")
def config() -> Settings:
    return Settings(app_name="naccbis-tests", db_url=NACCBIS_DB_URL)


@pytest.fixture(scope="session")
def db_url(config: Settings) -> str:
    return config.get_db_url()


@pytest.fixture(scope="session", autouse=True)
def create_db(db_url: str) -> None:
    url = make_url(db_url)
    postgres_url = url.set(database="postgres")
    print(postgres_url)
    pg_engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
    print("Creating database")
    with pg_engine.begin() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {url.database};"))
        conn.execute(text(f"CREATE DATABASE {url.database};"))

    pg_engine.dispose()

    engine = create_engine(db_url)
    print("Creating tables")
    with engine.begin() as conn:
        with open(SCHEMA_FILE) as f:
            conn.execute(text(f.read()))
    conn.close()


@pytest.mark.usefixtures("create_db")
@pytest.fixture(scope="session")
def db_conn(db_url: str) -> Iterator[Connection]:
    engine = create_engine(db_url)
    conn = engine.connect()
    yield conn
    conn.close()
