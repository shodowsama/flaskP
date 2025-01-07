from sqlalchemy import Table
from sqlalchemy import or_

from common.database import db_connect
from app.config.config import config
from app.settings import env

from model.user import User


dbsession,Base,engin = db_connect()

class Favorite(Base):
    __table__ = Table('favorite', Base.metadata, autoload_with=engin)

    def updata_status(self,article_id,user_id,canceled=0):
        favorite_data = dbsession.query(Favorite).filter_by(
            article_id = article_id,
            user_id = user_id
        ).first()

        if favorite_data is None:
            favorite = Favorite(
                article_id = article_id,
                user_id = user_id,
                canceled = canceled
            )
            dbsession.add(favorite)
        else:
            favorite_data.canceled = canceled
        dbsession.commit()

    def user_if_favorite(self,user_id,article_id):
        result = dbsession.query(Favorite.canceled).filter_by(
            user_id = user_id,
            article_id = article_id).first()
        
        if result is None:
            return 1
        else:
            return result[0]