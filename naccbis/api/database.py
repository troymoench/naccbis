from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from naccbis.common.settings import Settings

from .config import get_settings


def create_session(settings: Settings):
    SQLALCHEMY_DATABASE_URL = settings.get_db_url()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return sessionmaker(engine, autocommit=False, autoflush=False)


SessionLocal = create_session(get_settings())
