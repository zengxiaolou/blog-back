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


class UserCommentSerializers(serializers.ModelSerializer):
    """评论显示用户信息"""
    class Meta:
        model = user
        fields = ['id', 'username', 'avatar', 'github']


class ReplySerializer(serializers.ModelSerializer):
    """评论回复"""
    content = serializers.CharField(min_length=1, required=True)
    user = UserCommentSerializers(read_only=True)

    class Meta:
        model = Reply
        fields = ['comment', 'reply', 'created', 'content', 'user']


class CommentSerializer(serializers.ModelSerializer):
    """获取评论"""
    content = serializers.CharField(min_length=1, required=True)
    user = UserCommentSerializers(read_only=True)
    reply = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'created', 'user', 'reply']


class CreateCommentSerializer(serializers.ModelSerializer):
    """新增评论"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content = serializers.CharField(min_length=1, required=True)

    class Meta:
        model = Comment
        fields = ['article', 'content', 'user']


class CreateReplySerializer(serializers.ModelSerializer):
    """新增回复"""
    content = serializers.CharField(min_length=1, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reply
        fields = ['comment', 'reply', 'content', 'user']