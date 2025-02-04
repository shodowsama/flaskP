from sqlalchemy import Table
from sqlalchemy import or_,distinct

from common.database import db_connect
from app.config.config import config
from app.settings import env

from model.user import User
from model.favorite import Favorite
from model.feedback import Feedback


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
    
    def insert_article(self,user_id,title,article_content,drafted):
        article = Article(user_id = user_id,
                          title=title,
                          article_content=article_content,
                          drafted=drafted)
        dbsession.add(article)
        dbsession.commit()
        return article.id
    
    def update_article(self,article_id,title,
                       article_content,drafted,
                       label_name='',article_tag='',
                       article_type=''):
        row = dbsession.query(Article).filter_by(id=article_id).first()
        row.title = title
        row.article_content = article_content
        row.drafted = drafted
        row.label_name = label_name
        row.article_tag = article_tag
        row.article_type = article_type

        dbsession.commit()
        return article_id

    def update_article_header_image(self,article_id,article_image):
        row = dbsession.query(Article).filter_by(id=article_id).first()
        row.article_image = article_image
        dbsession.commit()
        return article_id


    def get_all_article_drafted(self,user_id):
        result = dbsession.query(Article).filter_by(user_id = user_id,
                                                    drafted=0).all()
        return result
    
    def get_one_article_drafted(self,article_id):
        result = dbsession.query(Article).filter_by(
            id = article_id,
            drafted = 0
        ).first()
        return result
    
    def get_article_by_userid(self,user_id):
        result = dbsession.query(Article).filter_by(user_id = user_id,
                                                    drafted=1).all()
        return self.app_path(result)
    

    def get_favorite_by_userid(self,user_id):
        result = dbsession.query(Article).join(
            Favorite,
            Favorite.article_id == Article.id
        ).filter(
            Favorite.user_id == user_id,
        ).order_by(
            Favorite.create_time.desc()
        ).all()
        return self.app_path(result)
    
    def get_feedback_by_userid(self,user_id):
        article_id_list = dbsession.query(
            distinct(Feedback.article_id)
            ).filter_by(user_id=user_id).subquery()
        
        result = dbsession.query(Article).filter(Article.id.in_(article_id_list)).all()
        return self.app_path(result)


        
    def app_path(self,article_list):
        for article in article_list:
            article.article_image = config[env].article_header_image_path + article.article_image
        return article_list

