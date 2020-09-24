from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.core.cache import caches

from .serializers import LikeSerializer


user = get_user_model()


class LikeView(APIView):
    """点赞相关"""

    def post(self, request):
        """获取点赞数和用户点赞相关信息"""
        pass
