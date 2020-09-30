"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/23-15:32
INSTRUCTIONS:   异步获取github用户信息
"""

from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task
import requests

from django.contrib.auth import get_user_model


from apis.users.models import Github

user = get_user_model()


@shared_task
def get_github_info(access_token: str = None, user_id: int = None, github_uid: str = None):
    """获取用户资料修改用户信息"""
    url = 'https://api.github.com/user'
    headers = {
        'Authorization': 'token ' + access_token
    }
    res = requests.get(url, headers=headers).json()
    avatar = res.get('avatar_url', '')
    github_url = res.get('html_url', '')
    github = Github.objects.filter(github_id=github_uid).first()
    if not github:
        github = Github()
    github.github_id = github_uid
    github.avatar = avatar
    github.homepage = github_url
    github.nickname = res.get('login', '')
    github.name = res.get('name', '')
    github.company = res.get('company', '')
    github.blog = res.get('blog', '')
    github.local = res.get('local', '')
    github.email = res.get('email', '')
    github.followers = res.get('followers', '')
    github.following = res.get('following', '')
    github.created = res.get('created_at', '')
    github.updated = res.get('updated_at', '')
    github.save()

    git_user = user.objects.get(pk=user_id)
    if git_user:
        if not git_user.avatar:
            git_user.avatar = avatar
        git_user.github = github_url
        git_user.github_info = github
        git_user.save()
