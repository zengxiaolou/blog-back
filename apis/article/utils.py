"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/24-16:20
INSTRUCTIONS:   小工具
"""
import redis
from main.settings import REDIS_HOST, REDIS_PORT


pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
redis_handle = redis.Redis(connection_pool=pool, db=2)