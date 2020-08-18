"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/18-13:31
INSTRUCTIONS:   小工具
"""

import re
import requests
from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


def generate_code() -> str:
    """生成6位数字验证码"""
    seeds = "1234567890"
    random_str = []
    for _ in range(6):
        random_str.append(choice(seeds))
    return "".join(random_str)


def jwt_response_payload_handler(token:str, user=None, request=None):
    """为返回的结果添加用户相关信息"""
    return {'token': token, 'username': user.username, 'id': user.id}


class CustomBackend(ModelBackend):
    """自定义用户验证"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if username.check_password(password):
                return user
        except Exception as e:
            return None