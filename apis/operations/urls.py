"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/15-14:36
INSTRUCTIONS:   用户操作
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet, CommentViewSet, ReplyViewSet

router = DefaultRouter()

router.register('like', LikeViewSet, basename='like')
router.register('comment', CommentViewSet, basename='comment')
router.register('reply', ReplyViewSet, basename='reply')

urlpatterns = [
    url('^', include(router.urls))
]