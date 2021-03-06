import datetime


from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.article.models import Category
from apis.utils.utils.other import redis_handle
from main.settings import REDIS_PREFIX, COUNT_PREFIX


class StatisticsView(APIView):
    """获取指标统计数据"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        total_view = redis_handle.get(REDIS_PREFIX + 'total_view') or 0
        total_like = redis_handle.get(REDIS_PREFIX + 'total_like') or 0
        total_user = redis_handle.get(COUNT_PREFIX + 'users') or 0
        total_comment = redis_handle.get(COUNT_PREFIX + 'comments') or 0

        today_view = redis_handle.hget(COUNT_PREFIX + 'view', str(today)) or 0
        today_like = redis_handle.hget(COUNT_PREFIX + 'like', str(today)) or 0
        today_user = redis_handle.hget(COUNT_PREFIX + 'user', str(today)) or 0
        today_comment = redis_handle.hget(COUNT_PREFIX + 'comment', str(today)) or 0

        everyday_view = redis_handle.hgetall(COUNT_PREFIX + 'view')
        everyday_like = redis_handle.hgetall(COUNT_PREFIX + 'like')
        everyday_user = redis_handle.hgetall(COUNT_PREFIX + 'user')
        everyday_comment = redis_handle.hgetall(COUNT_PREFIX + 'comment')

        data = {
            "today_view": today_view, "total_view": total_view, "everyday_view": everyday_view,
            "total_like": total_like, "today_like": today_like, "everyday_like": everyday_like,
            "total_user": total_user, "today_user": today_user, "everyday_user": everyday_user,
            "total_comment": total_comment, "today_comment": today_comment, "everyday_comment":everyday_comment

        }
        return Response(data, status=status.HTTP_200_OK)


class TagView(APIView):
    """获取标签分布"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        tags = redis_handle.hgetall(COUNT_PREFIX + 'tag')
        return Response(tags, status=status.HTTP_200_OK)