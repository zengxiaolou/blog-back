import datetime

from rest_framework import mixins, viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from apis.article.models import Article
from apis.operations.models import Comment, Reply
from .serializers import LikeSerializer, CommentSerializer, ReplySerializer, CreateCommentSerializer, \
    CreateReplySerializer, CommentLikeSerializer
from apis.utils.utils.other import redis_handle
from main.settings import REDIS_PREFIX, USER_PREFIX, COMMENT_PREFIX
from ..article.serialzers import ArchiveSerializer
from ..utils.pagination import MyPageNumberPagination

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
            redis_handle.zadd(USER_PREFIX + 'like:' + str(request.user.id), {kwargs['pk']: 0})
            redis_handle.incr(REDIS_PREFIX + "total_like", amount=1)
            data = {"result": '感谢点赞'}
        else:
            redis_handle.zrem(REDIS_PREFIX + "article_like:" + str(kwargs['pk']),  request.user.id)
            redis_handle.zrem(USER_PREFIX+'like:' + str(request.user.id), kwargs['pk'])
            redis_handle.incr(REDIS_PREFIX + "total_like", amount=-1)
            data = {"result": "已取消"}
        return Response(data, status=status.HTTP_200_OK)


class GetCommentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取评论列表"""
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('user__id',)
    search_fields = ('article__id',)
    queryset = Comment.objects.all()
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = self.get_paginated_response(serializer.data)
            for i in res.data['results']:
                name = COMMENT_PREFIX + 'like:' + str(i['id'])
                i['comment_like'] = redis_handle.zcard(name)
                i['is_like'] = True if request.user and redis_handle.exists(name) else False
            return res

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        redis_handle.incr(REDIS_PREFIX + 'article_comment:' + str(serializer.validated_data['article'].id), amount=1)
        serializer.save()


class GetReplyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('comment__id',)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = ()
    permission_classes = ()


class ReplyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Reply.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateReplySerializer

    def perform_create(self, serializer):
        redis_handle.incr(REDIS_PREFIX + 'article_comment:' + str(serializer.validated_data['comment'].article.id),
                          amount=1)
        serializer.save()


class UserLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """获取用户点赞数据"""
        user_id = request.user.id
        article_ids = redis_handle.zrevrange(USER_PREFIX + 'like:' + str(user_id), 0, -1)
        tmp = []
        for i in article_ids:
            tmp.append(int(i))
        articles = Article.objects.filter(id__in=tmp)
        Page = MyPageNumberPagination()
        page = Page.paginate_queryset(articles, request)
        if page is not None:
            serializer = ArchiveSerializer(page, many=True)
            return Page.get_paginated_response(serializer.data)
        serializer = ArchiveSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentLikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """用户对评论进行点赞和取消点赞"""
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer

    def perform_create(self, serializer):
        comment_id = serializer.validated_data['comment_id']
        redis_handle.zadd(COMMENT_PREFIX + 'like:' + str(comment_id), {self.request.user.id: 0})

    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs['pk']
        redis_handle.zrem(COMMENT_PREFIX + 'like:' + str(comment_id), self.request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
