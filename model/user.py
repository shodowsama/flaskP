from sqlalchemy import Table

from common.database import db_connect

dbsession,Base,engin = db_connect()

class User(Base):
    __table__= Table('compare_table',Base.metadata,autoload_with = engin)

    def get_one(self):
        return dbsession.query(User).first()