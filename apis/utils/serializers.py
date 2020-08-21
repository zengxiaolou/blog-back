"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/19-22:28
INSTRUCTIONS:   序列化数据并验证
"""

from rest_framework import serializers


class QiNiuUploadSerializer(serializers.Serializer):
    """七牛上传token"""
    name = serializers.ListField(child=serializers.CharField(min_length=2,max_length=30, required=True), required=True)
