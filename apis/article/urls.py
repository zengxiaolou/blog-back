"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:20
INSTRUCTIONS:   文件简介
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ArticleDocumentView, AddArticleViewSet, CategoryViewSet, TagViewSet, SaveArticleDraftViewSet, \
    ArticleDraftViewSet, GetTagViewSet, GetCategoryViewSet, ArchiveViewSet, HeatMapViewSet, GetViewAndLikeView, \
    GetLastYearDataView, ArticleOverViewSet, LikeView, ArticleCategoryTagViewSet

router = DefaultRouter()

router.register('search/article', ArticleDocumentView, basename='search/article')
router.register('category', CategoryViewSet, basename='category')
router.register('get/category', GetCategoryViewSet, basename='/get/category')
router.register('get/tag', GetTagViewSet, basename='get/tag')
router.register('tag', TagViewSet, basename='tag')
router.register('article', AddArticleViewSet, basename='article')
router.register('draft', SaveArticleDraftViewSet, basename='draft')
router.register('search/draft', ArticleDraftViewSet, basename='search/draft')
router.register('archive', ArchiveViewSet, basename='archive')
router.register('heat-map', HeatMapViewSet, basename='heat-map')
router.register('overview', ArticleOverViewSet, basename='overview')
router.register('category-tag', ArticleCategoryTagViewSet, basename='category-tag')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^last-data/$', GetLastYearDataView.as_view()),
    url(r"^like/$", LikeView.as_view()),
    url(r"^info/$", GetViewAndLikeView.as_view()),
]
