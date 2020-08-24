"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:20
INSTRUCTIONS:   文件简介
"""
from django.conf.urls import url, include
from rest_framework import routers

from .views import ArticleSearchView

router = routers.DefaultRouter()

router.register("search", ArticleSearchView, basename="search")

urlpatterns = [
    url('^search/', include(router.urls)),
]