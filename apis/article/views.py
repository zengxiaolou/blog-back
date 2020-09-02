from django.shortcuts import render
from django_elasticsearch_dsl_drf.constants import *
from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets, status, permissions
# from rest_framework.permissions import IsAdminUser

from .documents import ArticleDocument, ArticleDraftDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer,\
    SaveArticleDraftSerializer
from .models import Article, Category, Tags, ArticleDraft

from rest_framework.pagination import PageNumberPagination


class ArticleDocumentView(BaseDocumentViewSet):
    """已发表文章查询视图集"""
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')


class AddArticleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """新增文章相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AddArticleSerializer


class SaveArticleDraftViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """文章草稿箱相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaveArticleDraftSerializer
    queryset = ArticleDraft.objects.all()


class ArticleDraftViewSet(BaseDocumentViewSet):
    """草稿查询"""
    document = ArticleDraftDocument
    serializer_class = SaveArticleDraftSerializer
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """分类管理"""
    def get_permissions(self):
        if self.action == 'list':
            return []
        else:
            return [permissions.IsAdminUser()]

    def get_authenticate_header(self, request):
        if self.action == 'list':
            return []
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """标签管理"""
    def get_permissions(self):
        if self.action == 'list':
            return []
        else:
            return [permissions.IsAdminUser()]

    def get_authenticate_header(self, request):
        if self.action == 'list':
            return []
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()