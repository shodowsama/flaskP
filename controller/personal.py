from flask import Blueprint,render_template,request,session,jsonify,make_response,url_for
from model.article import Article
from model.user import User
from model.favorite import Favorite
from model.feedback import Feedback

from app.config.config import config
from app.settings import env
from common import response_message
from common.utils import compress_image

import random
import json
import time

personal = Blueprint('personal',__name__)


@personal.before_request
def personal_before_request():
    url = request.path
    is_login = session.get('is_login')
    if url.startswith('/personal') and 'new' and is_login != 'true':
        response = make_response('重新定向',302)
        response.headers['Location'] = url_for('index.home')
        return response
    
@personal.route('/personal')
def personal_center():

    type_name = request.args.get('type')
    if type_name is None:
        type_name = 'article'

    user_id = session.get('user_id')
    article = Article()

    if type_name == 'article':
        article_data = article.get_article_by_userid(user_id)
    elif  type_name == 'favorite':
        article_data = article.get_favorite_by_userid(user_id)
    elif  type_name == 'feedback':
        article_data = article.get_feedback_by_userid(user_id)
    else :
        return response_message.PersonalMessage.error('參數傳遞錯誤')
    
    user = User().find_by_userid(user_id)
    return render_template('personal_center.html',
                           article_data=article_data,
                           type_name = type_name,
                           active = type_name,
                           user=user)
