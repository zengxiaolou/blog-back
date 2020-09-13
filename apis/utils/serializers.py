"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/19-22:28
INSTRUCTIONS:   序列化数据并验证
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=30, min_length=5)

    @staticmethod
    def validate_email(email):
        """验证邮箱"""
        # 邮箱号码时候已注册
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError("邮箱号已被注册")
        # 验证码发送频率
        if cache.ttl('sms' + email) > 240:
            raise serializers.ValidationError("距上一次发送未超过60s")
        return email


class ResetEmailSerializer(serializers.Serializer):
    """重置密码获取验证码"""
    email = serializers.EmailField(required=True, max_length=30, min_length=5)

    @staticmethod
    def validate_email(email):
        if cache.ttl('sms' + email) > 240:
            raise serializers.ValidationError("距上一次发送未超过60s")
        return email


class QiNiuUploadSerializer(serializers.Serializer):
    """七牛上传token"""
    name = serializers.CharField(min_length=2, max_length=30, required=True)
