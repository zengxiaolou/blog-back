from django.db import models
from haystack.utils.geo import Point


class Article(models.Model):
    """文章"""
    title = models.CharField(max_length=100, verbose_name='文章标题')
    cover = models.CharField(max_length=255, verbose_name='文章封面')
    summary = models.TextField(verbose_name="文章简介")
    content = models.TextField(verbose_name='文章内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    str_num = models.IntegerField(default=0, verbose_name="文章字数")
    reading_time = models.IntegerField(default=0, verbose_name="阅读时间")
    views_num = models.IntegerField(default=0, verbose_name="浏览次数")
    comments_num = models.IntegerField(default=0, verbose_name="评论数量")
    like_num = models.IntegerField(default=0, verbose_name="点赞数量")

    def __str__(self):
        return self.title

