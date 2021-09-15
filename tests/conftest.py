import pytest
from naccbis.Common.settings import Settings


@pytest.fixture(scope="session")
def config():
    return Settings(app_name="naccbis-tests")


@pytest.fixture(scope="session")
def db_url(config):
    return config.get_db_url()
