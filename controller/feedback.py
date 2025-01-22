from flask import Blueprint,render_template,request,session,make_response,jsonify
from model.article import Article
from model.user import User
from model.favorite import Favorite
from model.feedback import Feedback

from app.config.config import config
from app.settings import env

from app.config.ue_config import UECONFIGE
from controller.feedback import compress_image
from common import response_message
from common.utils import model_to_json

import time
import json

feedback = Blueprint('feedback',__name__)

@feedback.before_request
def before_commit():
    if session.get('is_login') is None or session.get('is_login') != 'true':
        return {'status':9999,'data':'請登入'}


@feedback.route('/feedback',methods = ['get','post'])
def ueditor():
    param = request.args.get('action')
    if request.method == 'get' and param == 'config':
        return make_response(UECONFIGE)
    
    elif param == 'image':
        f= request.files.get('file')
        filename = f.filename
        suffix = filename.split('.')[-1]
        newname = time.strftime('%Y%m%d_%H%M%S.'+suffix)
        f.save('resource/upload/'+newname)

        source = dest = 'resource/upload/' + newname
        compress_image(source,dest,1200)
        result = {}
        result['state'] = 'success'
        result['url'] = '/upload/' + newname
        result['title'] = filename 
        result['original'] =  filename
        return jsonify(result)

@feedback.route('/feedback/add',methods = ['post'])
def add():
    request_data = json.loads(request.data)
    article_id = request_data.get('article_id')
    content = request_data.get('content').strip()
    ipaddr = request.remote_addr
    user_id = session.get('user_id')

    if len(content)<5 or len(content)>1000:
        return response_message.ArticleMessage.other('內容長度不符')
    
    feedback = Feedback()
    try:
        result = feedback.insert_comment(
            user_id=user_id,
            article_id=article_id,
            content=content,
            ipaddr=ipaddr
        )
        result= model_to_json(result)
        return response_message.ArticleMessage.success('評論成功')
    except Exception as e:
        return response_message.ArticleMessage.error('評論失敗')
    


@feedback.route('/feedback/reply',methods = ['post'])
def reply():
    request_data = json.loads(request.data)
    article_id = request_data.get('article_id')
    content = request_data.get('content').strip()
    ipaddr = request.remote_addr
    user_id = session.get('user_id')
    reply_id = request_data.get('reply_id')
    base_reply_id = request_data.get('base_reply_id')

    if len(content)<5 or len(content)>1000:
        return response_message.ArticleMessage.other('內容長度不符')
    
    feedback = Feedback()
    try:
        result = feedback.insert_reply(
                    user_id=user_id,
                    article_id=article_id,
                    content = content,
                    ipaddr = ipaddr,
                    reply_id=reply_id,
                    base_reply_id =base_reply_id
        )
        result= model_to_json(result)
        return response_message.ArticleMessage.success('評論成功')
    except Exception as e:
        return response_message.ArticleMessage.error('評論失敗')    