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

article = Blueprint('article',__name__)
label_types = config[env].label_types
article_types = config[env].article_types

@article.before_request
def article_before_request():
    url = request.path
    is_login = session.get('is_login')
    if url.startswith('/article') and 'new' in url and is_login != 'true':
        response = make_response('重新定向',302)
        response.headers['Location'] = url_for('index.home')
        return response

@article.route('/detail')
def article_detail():
    article_id = request.args.get('article_id')
    article = Article()
    article_content = article.get_article_detail(article_id)
    article_tag_str = article_content.article_tag
    article_tag_list = article_tag_str.split(',')

    user = User()
    user_info = user.find_by_userid(article_content.user_id)
    
    feedback_data_list = Feedback().get_fedback_user_list(article_id)


    is_favorite = 1

    if session.get('is_login') == 'True':
        user_id = session.get('user_id')
        is_favorite = Favorite().user_if_favorite(user_id,article_id)

    feedback_count = Feedback().get_article_feedback_count(article_id)

    about_article = article.find_about_article(article_content.label_name)


    return render_template('article-info.html',
                           article_content = article_content,
                           user_info = user_info,
                           is_favorite = is_favorite,
                           article_tag_list = article_tag_list,
                           about_article = about_article,
                           feedback_data_list = feedback_data_list,
                           feedback_count = feedback_count)

@article.route('/article/new')
def article_new():
    user_id = session.get('user_id')
    all_drafted = Article().get_all_article_drafted(user_id)
    return render_template('new-article.html',
                           label_types=label_types,
                           article_types=article_types,
                           article_tags = article_tags ,
                           all_drafted=all_drafted,
                           drafted_count = len(all_drafted))

@article.route('/article/drafted',methods=['post'])
def get_drafted_detail():
    request_data = json.loads(request.data)
    result = Article().get_one_article_drafted(request_data.get('id'))
    article_drafted = model_to_json(result)
    return response_message.ArticleMessage.success(article_drafted)


def get_article_request_param(request_data):
    user = User().find_by_userid(session.get('user_id'))
    title = request_data.get('title')
    article_content = request_data.get('article_content')
    return user,title,article_content



@article.route('/article/save',methods=['post'])
def article_save():
    request_data = json.loads(request.data)
    article_id = request_data.get('article_id')
    drafted = request_data.get('drafted')
    if article_id == -1 and drafted==0:
        user,title,article_content = get_article_request_param(request_data)
        if title == '':
            return response_message.ArticleMessage.other('請輸入標題')
        
        article_id = Article().insert_article(user.user_id,title,article_content,drafted)

        return response_message.ArticleMessage.drafted_success('草稿存儲成功',article_id)
    elif article_id>-1:
        user,title,article_content = get_article_request_param(request_data)
        if title == '':
            return response_message.ArticleMessage.other('請輸入標題')
        
        label_name = request_data.get('label_name')
        article_tag = request_data.get('article_tag')
        article_type = request_data.get('article_type')

        article_id = Article().update_article(
            article_id=article_id,
            title=title,
            article_content=article_content,
            drafted=drafted,
            label_name=label_name,
            article_tag= article_tag,
            article_type=article_type
        )

        return response_message.ArticleMessage.drafted_success('發布文章成功',article_id)



@article.route('/article/upload/article_header_image',methods=['post'])
def upload_article_header_image():
    f = request.files.get('header-image-file')
    filename = f.filename

    newname = 'article-header-'+newname
    suffix = filename.split('.')[-1]
    newname = time.strftime('%Y%m%d_%H%M%S.'+suffix)
    f.save('resource/upload/'+newname)

    source = dest = 'resource/upload/' + newname
    compress_image(source,dest,1200)

    article_id = request.form.get('article_id')
    Article().update_article_header_image(article_id,newname)


    result = {}
    result['state'] = 'success'
    result['url'] = '/upload/' + newname
    result['title'] = filename 
    result['original'] =  filename

    return jsonify(result)


@article.route('/article/random/header/image',methods=['post'])
def random_article_header_image():
    name = random.randint(1,539)
    newname = str(name) + '.jpg'

    article_id = request.form.get('article_id')
    Article().update_article_header_image(article_id,newname)


    result = {}
    result['state'] = 'success'
    result['url'] = '/images/headers/' + newname
    result['title'] = newname 
    result['original'] =  newname

    return jsonify(result)