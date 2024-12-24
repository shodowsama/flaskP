# 全域
class Config(object):
    db_url = 'mysql+pymysql://root:00000@127.0.0.1:3306/school_db'
    page_count = 10
    article_image_path = '/images/article/header/'


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