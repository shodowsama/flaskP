import logging
from logging.handlers import RotatingFileHandler
from app.config.config import config
from app.settings import env

def setlog():

    logging.basicConfig(level = config[env].LOG_LEVEL)
    
    file_log_handler = RotatingFileHandler('log/project.log',
                                           maxBytes=1024*1024*600,
                                           backupCount=10)
    
    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s')
    file_log_handler.setFormatter(log_formatter)

    logging.getLogger().addHandler(file_log_handler)

setlog()