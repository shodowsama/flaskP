from flask import Blueprint,render_template,request
from model.article import Article

from app.config.config import config
from app.settings import env

index = Blueprint('index',__name__)

label_type = {
    'auto_test':{'name':'自動化測試','selected':'selected'},
    'python':{'name':'python','selected':'noselected'},
    'java':{'name':'java','selected':'noselected'},
    'funny':{'name':'笑話','selected':'noselected'},
}



@index.route('/')
def home():
    page = request.args.get('page')
    article_type = request.args.get('article_type')

    if page in None:
        page = 1
    if article_type is None:
        article_type = 'recommend'

    article = Article()

    search_keyword = request.args.get('keyword')
    if search_keyword is not None:
        db_result = article.search_article(page,search_keyword)
    else:
        db_result = article.find_article(page,article_type)

    for article,nickname in db_result:
        article.label = label_type.get(article.label_name).get('name')

        article.create_time = str(article.create_time.month) + '.' + str(article.create_time.day)

        article.article_image = config[env].article_image_path + str(article.article_image)

        article.article_tag = article.article_tag.replace(',','.')

    start_num = request.args.get('start_num')
    if start_num is None:
        start_num = 0
    end_num = len(db_result)

    for k,v in label_type.items():
        if article_type == k:
            v['selected'] = 'selected'
        else:
            v['selected'] = 'noselected'

    return render_template('index.html',
                           result = db_result,
                           start_num = start_num,
                           end_num = end_num,
                           label_type = label_type)