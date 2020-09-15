"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/15-14:18
INSTRUCTIONS:   用户操作序列化
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apis.article.models import Article

user = get_user_model()


class ArticleLikeSerializer(serializers.ModelSerializer):
    """点赞"""
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=True)

    class Meta:
        model = Article
        fields = ['id', 'like_user', 'title', 'user']


class LikeSerializer(serializers.ModelSerializer):
    # article = ArticleLikeSerializer(many=True, read_only=True)

    class Meta:
        model = user
        fields = ['article']