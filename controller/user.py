import re
import json
import hashlib

from flask import Blueprint,make_response,session,request
from model.user import User
from common.utils import ImageCode
from common import response_message
from common.email_utils import get_email_code,send_email
from app.config.config import config
from app.settings import env


user = Blueprint('user',__name__)

@user.route('/123')
def getone():
    user = User()
    resul = user.get_one()

    return 'ok'

@user.route('/vcode')
def vcode():
    code,bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'

    session['vcode'] = code.lower()

    return response

@user.route('/ecode',methods = ['post'])
def emailcode():
    email = json.loads(request.data).get('email')

    if not re.match('.+@.+\..+',email):
        return response_message.UserMessage.other('無效郵件地址')
    
    code = get_email_code()

    try:
        send_email(email,code)
        session['ecode'] = code.lower()
        return response_message.UserMessage.success('郵件發送成功')
    except:
        return response_message.UserMessage.error('郵件發送失敗')

@user.route('/reg',methods = ['post'])
def register():
    request_data = json.loads(request.data)
    username = request_data.get('username')
    password = request_data.get('password')
    s_password = request_data.get('second_password')
    eocde = request_data.get('eocde')

    if eocde.lower() != session.get('ecode'):
        return response_message.UserMessage.error('驗證碼錯誤')
    
    if not re.match('.+@.+\..+',username):
        return response_message.UserMessage.error('無效信箱地址')
    
    if password != s_password:
        return response_message.UserMessage.error('密碼不一致')
    
    user = User()
    if len(user.find_by_username(username=username))>0:
        return response_message.UserMessage.error('用戶名已經存在')
    
    password = hashlib.md5(password.encode()).hexdigest()
    result = user.do_register(username=username,password=password)

    return response_message.UserMessage.success('註冊成功')

@user.route('/login',methods = ['post'])
def login():
    request_data = json.loads(request.data)
    username = request_data.get('username')
    password = request_data.get('password')
    vcode = request_data.get('vcode')

    if vcode != session.get('vcode'):
        return response_message.UserMessage.success('驗證碼錯誤')
    
    password = hashlib.md5(password.encode()).hexdigest()
    user = User()
    result = user.find_by_username(username)
    if len(result) == 1 and result[0].password == password:
        session['is_login'] = 'true'
        session['user_id'] = result[0].user_id
        session['username'] = username
        session['nickname'] = result[0].nickname
        session['picture'] = config[env].user_header_image_path + result[0].picture

        response = make_response(response_message.UserMessage.success('登陸成功'))
        response.set_cookie('username',username,max_age=30*24*3600)

        return response
    
    else:
        return response_message.UserMessage.error('用戶名錯誤')
    

@user.route('/logout')
def logout():
    session.clear()
    response = make_response('登出並重新定位',302)
    response.headers['Location'] = url_for('index.home')

    response.delete_cookie('username')
    return response