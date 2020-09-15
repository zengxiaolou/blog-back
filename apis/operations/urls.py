"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/15-14:36
INSTRUCTIONS:   用户操作
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apis.operations.views import LikeViewSet

router = DefaultRouter()
router.register('like', LikeViewSet, basename='like')


urlpatterns = [
    url('^', include(router.urls))
]