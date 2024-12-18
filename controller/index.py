from flask import Blueprint,render_template,request

index = Blueprint('index',__name__)

@index.route('/')
def home():
    page = request.args.get('page')
    article_type = request.args.get('article_type')

    if page in None:
        page = 1
    if article_type is None:
        article_type = 'recommend'

    article = Article()
    db_result = article.find_article(page,article_type)






    return render_template('index.html',result = db_result)