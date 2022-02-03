from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from wopweb.config import cfg


Base = declarative_base()

db_engine = None
db_session = None


def get_db(db=None):
    global db_engine
    global db_session
    global Base

    if not db:
        db = cfg.db

    db_engine = create_engine(db)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=db_engine))
    Base.query = db_session.query_property()


def init_db(engine=None):
    global db_engine
    if not engine:
        engine = db_engine

    import wopweb.models
    Base.metadata.create_all(bind=engine)


def close_db():
    global db_session
    if db_session:
        db_session.remove()
