from flask import Flask

import os



def create_app():
    app = Flask(__name__,
                template_folder='../template',
                static_url_path='/',
                static_folder='../static')
    
    init_bp(app)
    app.config['SECRET_KEY'] = os.urandom(24)

    return app

def init_bp(app):
    from controller.user import user
    app.register_blueprint(user)

    from controller.index import index
    app.register_blueprint(index)

    from controller.article import article
    app.register_blueprint(article)

    from controller.feedback import feedback
    app.register_blueprint(feedback)

    from controller.personal import personal
    app.register_blueprint(personal)