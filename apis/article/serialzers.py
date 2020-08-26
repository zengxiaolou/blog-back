"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:03
INSTRUCTIONS:   文章序列化
"""
import json
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import ArticleDocument
from .models import Article


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta(object):
        document = ArticleDocument
        fields = (
            'title', 'cover', 'summary', 'content'
        )


class AddArticleSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cover = serializers.CharField(min_length=30, max_length=500, required=True)
    title = serializers.CharField(min_length=2, max_length=50, required=True)

    class Meta:
        model = Article
        fields = ('title', 'content', 'cover', 'summary', 'created')