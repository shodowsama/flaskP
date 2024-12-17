# 全域
class Config(object):
    db_url = 'mysql+pymysql://root:00000@127.0.0.1:3306/school_db'


# 測試
class TestC(Config):
    if_echo = True



# 開發
class ProductionC(Config):
    if_echo = False


config = {
    'test':TestC,
    'prop':ProductionC
}