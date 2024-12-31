import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config.config import config
from app.settings import env

def get_email_code():
    list = random.sample(string.ascii_letters + string.digits,6)
    return ''.join(list)

def send_email(email,code):
    email_name = config[env].email_name
    passwd = config[env].passwd

    msg_to = email

    content = """
    驗證碼是: <h1 style='color:red'>{}</h1>
    """.format(code)

    msg = MIMEMultipart()
    msg['Subject'] = '驗證碼'
    msg['From'] = email_name
    msg['To'] = msg_to

    msg.attach(MIMEText(content,'html','utf-8'))
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login(email_name,passwd)
    s.sendmail(email_name,msg_to,msg.as_string())
