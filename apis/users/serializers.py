"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/18-13:09
INSTRUCTIONS:   用户信息序列化
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息
    """

    class Meta:
        model = User
        fields = '__all__'
