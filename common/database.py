from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session,declarative_base
from app.config.config import config
from app.settings import env


def db_connect():
    engin = create_engine(config[env].db_url , echo = config[env].if_echo)

    session = sessionmaker(engin)

    dbsession = scoped_session(session)

    Base = declarative_base()

    return dbsession,Base,engin
 