"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/13-17:33
INSTRUCTIONS:   其他常用小工具
"""
from random import choice
import redis
from main.settings import REDIS_HOST, REDIS_PORT


pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
redis_handle = redis.Redis(connection_pool=pool, db=2)


def generate_code() -> str:
    """生成6位数字的验证码"""
    seeds = "1234567890"
    random_str = []
    for i in range(6):
        random_str.append(choice(seeds))
    return "".join(random_str)


