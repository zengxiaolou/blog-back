from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from apis.article.models import Article

user = get_user_model()


class Comment(models.Model):
    """评论"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article", verbose_name="文章")
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="commenter", verbose_name="评论者")
    content = models.TextField(verbose_name="评论内容")
    created = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created']


class Reply(models.Model):
    """回复"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply', verbose_name="评论")
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="reply_set",
                              verbose_name="回复对象")
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="reply", verbose_name="回复者")
    created = models.DateTimeField(default=datetime.now, verbose_name="回复时间")
    content = models.TextField(verbose_name="回复内容")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created']


class Subscribe(models.Model):
    """订阅邮箱"""
    email = models.EmailField(verbose_name='订阅邮箱', unique=True)

    def __str__(self):
        return self.email