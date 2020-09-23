"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/23-15:32
INSTRUCTIONS:   异步获取github用户信息
"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
import requests

from django.contrib.auth import get_user_model

user = get_user_model()


@shared_task
def get_github_info(access_token: str, user_id: int):
    """获取用户资料修改用户信息"""
    url = 'https://api.github.com/user'
    headers = {
        'Authorization': 'token ' + access_token
    }
    res = requests.get(url, headers=headers).json()
    avatar = res.get('avatar_url', '')
    github_url = res.get('url', '')
    git_user = user.objects.get(pk=user_id)
    if git_user:
        git_user.avatar = avatar
        git_user.github = github_url
        git_user.save()
