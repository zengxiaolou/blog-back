import logging

from django.db.models import Count
from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apis.utils.pagination import MyPageNumberPagination
from .documents import ArticleDocument, ArticleDraftDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer, \
    SaveArticleDraftSerializer, ArticleDraftDocumentSerializer, ArchiveSerializer, ArticleOverViewSerializer, \
    ArticleContentSerializer
from .models import Article, Category, Tags, ArticleDraft
from apis.utils.utils.other import redis_handle
from main.settings import REDIS_PREFIX

logger = logging.getLogger('mdjango')

like_view_parm = [openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, description='用户ID', type=openapi.TYPE_NUMBER),
                  openapi.Parameter(name='article_id', in_=openapi.IN_QUERY, description="文章ID", type=openapi.TYPE_NUMBER)]


class ArticleDocumentView(BaseDocumentViewSet):
    """已发表文章查询视图集"""
    document = ArticleDocument
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleDocumentSerializer
    pagination_class = MyPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend,
    ]
    ordering_fields = {
        'created': 'created'
    }
    ordering = ('-created',)
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        redis_handle.incr(REDIS_PREFIX + 'view:' + str(instance.id), amount=1)
        redis_handle.incr(REDIS_PREFIX + "total_view", amount=1)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = self.get_paginated_response(serializer.data)
            for i in res.data['results']:
                view = redis_handle.get(REDIS_PREFIX + 'view:' + str(i['id']))
                i['view'] = view if view else 0
                i['like'] = redis_handle.zcard(REDIS_PREFIX + 'article_like:' + str(i['id']))
            return res

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArchiveViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章归档"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArchiveSerializer
    queryset = Article.objects.all()


class HeatMapViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章数量与日期"""
    serializer_class = ArchiveSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('created',)

    def get_queryset(self):
        return Article.objects.values('created').annotate(test=sum('created')).all()


class ArticleOverViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章概览数据"""
    serializer_class = ArticleOverViewSerializer
    permission_classes = ()
    authentication_classes = ()
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = self.get_paginated_response(serializer.data)
            for i in res.data['results']:
                view = redis_handle.get(REDIS_PREFIX + 'view:' + str(i['id']))
                i['view'] = view if view else 0
                i['like'] = redis_handle.zcard(REDIS_PREFIX + 'article_like:' + str(i['id']))
            return res
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddArticleViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """新增文章相关"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleContentSerializer
        return AddArticleSerializer

    def perform_create(self, serializer):
        serializer.save()
        category = serializer.validated_data["category"]
        category.num += 1
        category.save()
        redis_handle.incr(REDIS_PREFIX + "total_article", amount=1)


class SaveArticleDraftViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """文章草稿箱相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaveArticleDraftSerializer
    queryset = ArticleDraft.objects.all()


class ArticleDraftViewSet(BaseDocumentViewSet):
    """草稿查询"""
    document = ArticleDraftDocument
    serializer_class = ArticleDraftDocumentSerializer
    pagination_class = MyPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')


class GetCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """分类管理"""

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetTagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class TagViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """标签管理"""

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class GetViewAndLikeView(APIView):
    """获取文章总数、浏览总数、点赞总数"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            total_like = redis_handle.get(REDIS_PREFIX + "total_like")
            total_article = redis_handle.get(REDIS_PREFIX + "total_article")
            total_view = redis_handle.get(REDIS_PREFIX + "total_view")
            data = {'total_like': total_like, "total_article": total_article, "total_view": total_view}
        except Exception as e:
            return Response({"data": str(e.args)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


class GetLastYearDataView(APIView):
    """获取最近一年文章数据"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        article = Article.objects.count()
        queryset = Article.objects.dates('create', 'day').values('create').annotate(count=Count('id'))
        data = {
            "results": {
                'article': article,
                'date': queryset
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class LikeView(APIView):
    """文章点赞相关"""
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(operation_description='获取文章点赞数', manual_parameters=like_view_parm)
    def get(self, request, *args, **kwargs):
        """获取所有点赞数或指定文章的点赞数"""
        article_id = request.query_params.get('article_id', '')
        user_id = request.query_params.get('user_id', '')
        article_name = "article_like:" + str(article_id)
        view_name = "view:" + str(article_id)
        try:
            if article_id and user_id:
                article_like = redis_handle.zcard(REDIS_PREFIX + article_name)
                view = redis_handle.get(REDIS_PREFIX + view_name)
                view = view if view else 0
                flag = redis_handle.zrank(REDIS_PREFIX + article_name, user_id)
                data = {"total": article_like, 'view': view, "flag": flag}
            elif article_id:
                article_like = redis_handle.zcard(REDIS_PREFIX + article_name)
                view = redis_handle.get(REDIS_PREFIX + view_name)
                data = {"total": article_like, 'view': view}
            else:
                total_like = redis_handle.get(REDIS_PREFIX + "total_like")
                data = {"total": total_like}
        except Exception as e:
            return Response({'data': '数据查询失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)