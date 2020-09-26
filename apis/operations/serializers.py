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
from apis.operations.models import Comment, Reply

user = get_user_model()


class LikeSerializer(serializers.Serializer):
    """点赞"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like = serializers.BooleanField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    """评论"""
    content = serializers.CharField(min_length=1, required=True)

    class Meta:
        model = Comment
        fields = ['article', 'content', 'created', 'user']
        depth = 1


class ReplySerializer(serializers.ModelSerializer):
    """评论回复"""
    content = serializers.CharField(min_length=1, required=True)

    class Meta:
        model = Reply
        fields = "__all__"
        depth = 1