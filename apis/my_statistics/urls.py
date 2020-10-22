"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/10/21-23:06
INSTRUCTIONS:   文件简介
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apis.my_statistics.views import StatisticsView, TagView

router = DefaultRouter()

urlpatterns = [
    url('', include(router.urls)),
    url(r"^base/$", StatisticsView.as_view()),
    url(r"^tag/$", TagView.as_view())
]