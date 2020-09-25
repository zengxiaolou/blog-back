from rest_framework import mixins, viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

from apis.article.models import Article
from .serializers import LikeSerializer
from apis.utils.utils.other import redis_handle
from main.settings import REDIS_PREFIX

user = get_user_model()


class LikeViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """点赞相关"""
    serializer_class = LikeSerializer
    queryset = Article.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['like']:
            redis_handle.zadd(REDIS_PREFIX + "article_like:" + str(kwargs['pk']), {request.user.id: 0})
            redis_handle.incr(REDIS_PREFIX + "total_like", amount=1)
            data = {"result": '感谢点赞'}
        else:
            redis_handle.zrem(REDIS_PREFIX + "article_like:" + str(kwargs['pk']),  request.user.id)
            redis_handle.incr(REDIS_PREFIX + "total_like", amount=-1)
            data = {"result": "已取消"}
        return Response(data, status=status.HTTP_200_OK)

