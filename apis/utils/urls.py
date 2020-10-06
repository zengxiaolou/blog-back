"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/19-22:06
INSTRUCTIONS:   小工具
"""
from django.conf.urls import url, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# 短信
router.register('sms', PhoneViewSet, basename='sms')

urlpatterns = [
    url(r'^captcha/', include('extract_apps.rest_captcha.urls')),
    url(r'', include(router.urls)),
    url(r'^check-captcha/$', CheckCaptcha.as_view()),
    url(r'^qiniu-token/$', GetQiNiuToken.as_view()),
    url(r'^get-sms/$', EmailView.as_view())
]
