# 全域
class Config(object):
    db_url = 'mysql+pymysql://root:00000@127.0.0.1:3306/school_db'
    page_count = 10
    article_image_path = '/images/article/header/'

    email_name = '123@gmail.com'
    passwd = '123456' # 授權碼

    user_header_image_path = '/images/headers/'

    REDIS_HOST = '192.168.1.129'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    REDIS_POLL = 10
    REDIS_DB = 2
    REDIS_DECODE_RESPONSE = True


# 測試
class TestC(Config):
    if_echo = True
    LOG_LEVEL = 'DEBUG'


# 開發
class ProductionC(Config):
    if_echo = False
    LOG_LEVEL = 'INFO'


config = {
    'test':TestC,
    'prop':ProductionC
}