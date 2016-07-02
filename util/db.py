from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine(settings):
    db_url = settings.get_db_url()
    engine = create_engine(db_url, echo=settings.debug)
    return engine


def get_db_session(settings):
    eng = get_db_engine(settings)
    Session = sessionmaker(bind=eng)
    return Session
