from sqlalchemy import Table

from common.database import db_connect
from app.config.config import config
from app.settings import env

dbsession,Base,engin = db_connect()

class Article(Base):
    __table__ = Table('article', Base.metadata, autoload_with=engin)

    def find_article(self,page,article_type='recommend'):
        if page < 1:
            page = 1

        count = int(page) * config[env].page_count
        if article_type == 'recommend':
            result = dbsession.query(Article,User.nickname).join(
                User,User.userid == Article.userid
            ).filter(
                Article.drafted == 1 
            ).order_by(
                Article.browse_num.desc()
                ).limit(count).all()
        else:
            result = dbsession.query(Article,User.nickname).join(
                User,User.userid == Article.userid
            ).filter(
                Article.label_name == article_type,
                Article.drafted == 1 
            ).order_by(
                Article.browse_num.desc()
                ).limit(count).all()