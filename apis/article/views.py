from django.shortcuts import render
from drf_haystack.viewsets import HaystackViewSet

from .models import Article
from .serialzers import ArticleSerializer


class ArticleSearchView(HaystackViewSet):
    index_models = [Article]
    serializer_class = ArticleSerializer