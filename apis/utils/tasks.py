"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/13-17:43
INSTRUCTIONS:   文件简介
"""
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mails(theme: str, code: str, account: str):
    """发送邮件"""
    send_mail(
        theme,
        '您的验证码为\n ' + code + "\n有效期为5分钟",
        '18328457630@163.com',
        ['18328457630@163.com', account],
        fail_silently=False
    )
