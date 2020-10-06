"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/19-22:28
INSTRUCTIONS:   序列化数据并验证
"""
import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache

from main.settings import REGEX_MOBILE

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


class SmsSerializer(serializers.Serializer):
    """手机短信"""
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)

    @staticmethod
    def validate_mobile(mobile):
        """验证手机号"""

        # 手机号是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号已注册")

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号格式不正确")

        # 短信发送频率
        if cache.ttl('sms' + mobile) > 240:
            raise serializers.ValidationError("距上一次发送未超过60s")

        return mobile
