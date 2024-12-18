from flask import Blueprint
from model.user import User

user = Blueprint('user',__name__)

@user.route('/123')
def getone():
    user = User()
    resul = user.get_one()

    return 'ok'