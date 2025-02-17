from sqlalchemy import Table
from sqlalchemy import or_,func

from common.database import db_connect
from common.utils import model_to_json
from app.config.config import config
from app.settings import env

from model.user import User

dbsession,Base,engin = db_connect()

class Feedback(Base):
    __table__ = Table('comment', Base.metadata, autoload_with=engin)

    def get_fedback_user_list(self,article_id):
        final_data_list = []
        feedback_list = self.find_feedback_by_article_id(article_id)
        for feedback  in feedback_list:
            user = User()
            reply_list = []
            all_reply = self.find_reply_by_replyid(base_reply_id=feedback.id)
            feedback_user = user.find_by_userid(feedback.user_id)
            for reply in all_reply:
                reply_content_with_user = {}
                from_user_data = user.find_by_userid(reply.user_id)
                to_user_reply_data = self.find_reply_by_id(reply.reply_id)
                to_user_data = user.find_by_userid(to_user_reply_data[0].user_id)

                reply_content_with_user['from_user'] = model_to_json(from_user_data)
                reply_content_with_user['to_user'] = model_to_json(to_user_data)
                reply_content_with_user['content'] = model_to_json(reply)

                reply_list.append(reply_content_with_user)

            every_feedback_data = model_to_json(feedback)
            every_feedback_data.update(model_to_json(feedback_user))
            every_feedback_data['reply_list'] = reply_list
            final_data_list.append(every_feedback_data)

        return final_data_list


    def find_feedback_by_article_id(self,article_id):
        result = dbsession.query(Feedback).filter_by(
            article_id = article_id,
            reply_id = 0,
            base_reply_id = 0
        ).order_by(
            Feedback.id.desc()
        ).all()
        return result
    
    def find_reply_by_replyid(self,base_reply_id):
        result = dbsession.query(Feedback).filter_by(
            base_reply_id = base_reply_id
        ).order_by(
            Feedback.id.desc()
        ).all()
        return result        
    
    def find_reply_by_id(self,id):
        result = dbsession.query(Feedback).filter_by(
            Feedback.id == id
        ).order_by(
            Feedback.id.desc()
        ).all()
        return result       

    def get_article_feedback_count(self,article_id):
        result = dbsession.query(Feedback).filter_by(
            article_id = article_id,
            reply_id = 0,
            base_reply_id = 0
        ).count()
        return result
    
    def insert_comment(self,user_id,article_id,content,ipaddr):
        feedback_max_floor = dbsession.query(
            func.max(Feedback.floor_number).label('max_floor')
            ).filter_by(article_id=article_id).first()
        if feedback_max_floor.max_floor == 0 or feedback_max_floor.max_floor is None:
            feedback = Feedback(user_id=user_id,
                                article_id=article_id,
                                content = content,
                                ipaddr = ipaddr,
                                floor_number=1,
                                reply_id=0,
                                base_reply_id =0)
        else:
            feedback = Feedback(user_id=user_id,
                                article_id=article_id,
                                content = content,
                                ipaddr = ipaddr,
                                floor_number=int(feedback_max_floor) + 1,
                                reply_id=0,
                                base_reply_id =0)     
        dbsession.add(feedback)
        dbsession.commit()   
        return feedback
    
    def insert_reply(self,article_id,user_id,content,ipaddr,reply_id,base_reply_id):
        feedback = Feedback(user_id=user_id,
                    article_id=article_id,
                    content = content,
                    ipaddr = ipaddr,
                    reply_id=reply_id,
                    base_reply_id =base_reply_id)     
        dbsession.add(feedback)
        dbsession.commit() 