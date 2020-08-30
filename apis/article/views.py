from django.shortcuts import render
from django_elasticsearch_dsl_drf.constants import *
from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.permissions import IsAdminUser

from .documents import ArticleDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer
from .models import Article, Category, Tags

from rest_framework.pagination import PageNumberPagination

class ArticleDocumentView(BaseDocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary')


class AddArticleViewSet(APIView):
    permission_classes = (permissions.IsAdminUser,)
    @swagger_auto_schema(request_body=AddArticleSerializer, responses={201: AddArticleSerializer})
    def post(self, request, *args, **kwargs):
        serializer = AddArticleSerializer(data=request.data)
        if serializer.is_valid():
            article_orm = Article(**serializer.validated_data)
            article_orm.save()
            data = {
                "msg": "添加成功"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """分类管理"""
    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return [permissions.IsAdminUser()]
        else:
            return []

    def get_authenticate_header(self, request):
        if self.action == 'list':
            return []
    # authentication_classes =
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """标签管理"""
    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = []
    #     else:
    #         permission_classes = [permissions.IsAdminUser()]
        # return [permission() for permission in permission_classes]

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()