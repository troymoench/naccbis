from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings
from naccbis.common.settings import Settings


def create_session(settings: Settings):
    SQLALCHEMY_DATABASE_URL = settings.get_db_url()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = create_session(get_settings())
