from flask import Blueprint
from model.user import User

user = Blueprint('user',__name__)

@user.route('/')
def getone():
    user = User()
    resul = user.get_one()
    print(resul.tb_Origin)
    return 'ok'