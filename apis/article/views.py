from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response

from apis.utils.pagination import MyPageNumberPagination
from .documents import ArticleDocument, ArticleDraftDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer, \
    SaveArticleDraftSerializer, ArticleDraftDocumentSerializer
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