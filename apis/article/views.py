from datetime import datetime

from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, Trunc
from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.utils.pagination import MyPageNumberPagination
from .documents import ArticleDocument, ArticleDraftDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer, \
    SaveArticleDraftSerializer, ArticleDraftDocumentSerializer, ArchiveSerializer
from .models import Article, Category, Tags, ArticleDraft


class ArticleDocumentView(BaseDocumentViewSet):
    """已发表文章查询视图集"""
    document = ArticleDocument
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleDocumentSerializer
    pagination_class = MyPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')


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


class AddArticleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """新增文章相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AddArticleSerializer

    def perform_create(self, serializer):
        serializer.save()
        category = serializer.validated_data["category"]
        category.num += 1
        category.save()


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
        article = Article.objects.count()
        view = Article.objects.all().aggregate(views=Sum('views_num'), likes=Sum('like_num'))
        views, like = view['views'], view['likes']
        data = {
            "results": {
                'article': article,
                'view': views,
                'like': like
            }
        }
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
