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
from rest_framework.validators import UniqueValidator

from .documents import ArticleDocument
from .models import Article, Category, Tags, ArticleDraft


class CategorySerializer(serializers.ModelSerializer):
    """文章分类"""
    category = serializers.CharField(max_length=10, min_length=2, required=True,
                                     validators=[UniqueValidator(queryset=Category.objects.all())])
    num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    """文章标签"""
    tag = serializers.CharField(max_length=10, min_length=2, required=True,
                                validators=[UniqueValidator(queryset=Tags.objects.all())])
    num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tags
        fields = '__all__'


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta(object):
        document = ArticleDocument


class AddArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cover = serializers.CharField(min_length=2, max_length=500, required=True)
    title = serializers.CharField(min_length=2, max_length=50, required=True)
    str_num = serializers.IntegerField(required=True)

    class Meta:
        model = Article
        fields = ['summary', 'cover', 'title', 'content', 'user', 'category', 'tag', 'str_num']


class SaveArticleDraftSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ArticleDraft
        fields = ['summary', 'cover', 'title', 'content', 'user']
