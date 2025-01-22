import random
from sqlalchemy import Table

from app.config.config import config
from app.settings import env

from common.database import db_connect

dbsession,Base,engin = db_connect()

class User(Base):
    __table__= Table('compare_table',Base.metadata,autoload_with = engin)

    def get_one(self):
        return dbsession.query(User).first()
    
    def find_by_username(self,username):
        return dbsession.query(User).filter_by(username = username).all()
    
    def do_register(self,username,password):
        nickname = username.split('@')[0]
        picture_num = random.randint(1,539)
        picture = str(picture_num) + '.jpg'

        job = 'None'
        user = User(username = username,
                    password = password,
                    nickname = nickname,
                    picture = picture,
                    job = job)
        
        dbsession.add(user)
        dbsession.commit()
        return user
    
    def find_by_userid(self,user_id):
        user_info = dbsession.query(User).filter_by(user_id = user_id).first()

        if user_info.picture.startswith(config[env].user_header_image_path):
            return user_info
        else:
            user_info.picture = config[env].user_header_image_path + user_info.picture
            return user_info