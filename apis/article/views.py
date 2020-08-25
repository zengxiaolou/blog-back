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


from .documents import ArticleDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer


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

    @swagger_auto_schema(request_body=AddArticleSerializer, responses={200: AddArticleSerializer})
    def post(self, request, *args, **kwargs):
        serializer = AddArticleSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            cover = serializer.validated_data['cover']
            content = serializer.validated_data['content']
            summary = serializer.validated_data['summary']
            article = ArticleDocument(title=title, cover=cover, content=content, summary=summary)
            article.save()
            data = {
                "msg": "添加成功"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)