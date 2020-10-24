"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/10/24-12:39
INSTRUCTIONS:   文件简介
"""
from celery import shared_task
from django.core.mail import send_mail

from apis.operations.models import Subscribe


@shared_task
def send_mails(theme: str, title: str, url: str):
    """发送订阅邮件"""
    subscribe = Subscribe.objects.all()
    emails = []
    if subscribe:
        for i in subscribe:
            emails.append(i.email)
    emails.append('18328457630@163.com')
    send_mail(
        theme,
        '您订阅的破栈（http://blog.messstack.com）有新文章发布\n标题： ' + title + "\n地址：" + url,
        '18328457630@163.com',
        emails,
        fail_silently=False
    )