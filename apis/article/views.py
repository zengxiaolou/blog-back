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
from .models import Article


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

    @swagger_auto_schema(request_body=ArticleDocumentSerializer, responses={200: AddArticleSerializer})
    def post(self, request, *args, **kwargs):
        serializer = AddArticleSerializer(data=request.data)
        if serializer.is_valid():
            article_orm = Article(**serializer.validated_data)
            article_orm.save()
            # serializer.validated_data['id'] = article_orm.id
            # serializer.validated_data['created'] = article_orm.created
            # article = ArticleDocument(**serializer.validated_data)
            # article.save()
            data = {
                "msg": "添加成功"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)