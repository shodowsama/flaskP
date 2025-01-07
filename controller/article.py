from flask import Blueprint,render_template,request,session
from model.article import Article
from model.user import User
from model.favorite import Favorite
from model.feedback import Feedback

from app.config.config import config
from app.settings import env

article = Blueprint('article',__name__)

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

    about_article = article.find_about_article(article_content.label_name)


    return render_template('article-info.html',
                           article_content = article_content,
                           user_info = user_info,
                           is_favorite = is_favorite,
                           article_tag_list = article_tag_list,
                           about_article = about_article,
                           feedback_data_list = feedback_data_list)
