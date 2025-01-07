from sqlalchemy import Table
from sqlalchemy import or_

from common.database import db_connect
from app.config.config import config
from app.settings import env

from model.user import User


dbsession,Base,engin = db_connect()

class Article(Base):
    __table__ = Table('article', Base.metadata, autoload_with=engin)

    def find_article(self,page,article_type='recommend'):
        if int(page) < 1:
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
        return result 
            
    def search_article(self,page,keyword):
        if int(page) < 1:
            page = 1
        count = int(page) * config[env].page_count

        result = dbsession.query(Article,User.nickname).join(
                User,User.userid == Article.userid
            ).filter(
                or_(Article.title.like('%'+keyword +'%'),
                    Article.article_content.like('%'+keyword +'%'))
            ).order_by(
                Article.browse_num.desc()
                ).limit(count).all()
        return result
    
    def get_article_detail(self,article_id):
        return dbsession.query(Article).filter_by(id = article_id).first()
    
    def find_about_article(self,label_name):
        return dbsession.query(Article).filter_by(
            label_name=label_name
        ).order_by(
            Article.browse_num.desc()
        ).limit(5)