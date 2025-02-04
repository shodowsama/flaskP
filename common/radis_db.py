from app.config.config import config
from app.settings import env
import redis

def redis_connect():
    redis_config = config[env]
    pool = redis.ConnectionPool(
        host = redis_config.REDIS_HOST
        port = redis_config.REDIS_PORT
        db = redis_config.REDIS_DB
        decode_responses = redis_config.REDIS_DECODE_RESPONSE
    )

    return redis.Redis(connection_pool=pool)