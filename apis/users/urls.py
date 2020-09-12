"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/18-13:03
INSTRUCTIONS:   用户信息urls
"""

from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

# 配置用户信息相关url
router.register(r'details', UserViewSet, basename='details')

urlpatterns = [
    url(r'^login/$', obtain_jwt_token),
    url(r'^', include(router.urls))
]
