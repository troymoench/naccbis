import pytest
from naccbis.Common.settings import Settings

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url, Connection

TEST_DBNAME = "naccbisdb_test"
SCHEMA_FILE = "db/schema_dump_2021_09_14.sql"


@pytest.fixture(scope="session")
def config() -> Settings:
    return Settings(app_name="naccbis-tests")


@pytest.fixture(scope="session")
def db_url(config: Settings) -> str:
    url = make_url(config.get_db_url())
    # for now, hard code the testing database
    testing_url = URL.create(
        drivername=url.drivername,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database=TEST_DBNAME,
        query=url.query,
    )
    return str(testing_url)


@pytest.fixture(scope="session", autouse=True)
def create_db(db_url: str) -> None:
    url = make_url(db_url)
    postgres_url = URL.create(
        drivername=url.drivername,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database="postgres",
        query=url.query,
    )
    print(postgres_url)
    engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE IF EXISTS {TEST_DBNAME};")
        conn.execute(f"CREATE DATABASE {TEST_DBNAME};")


@pytest.fixture(scope="session")
def db_conn(db_url: str) -> Connection:
    engine = create_engine(db_url)
    conn = engine.connect()
    print("Creating tables")
    with conn.begin():
        with open(SCHEMA_FILE) as f:
            conn.execute(text(f.read()))

    yield conn
    conn.close()
