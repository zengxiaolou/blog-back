"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/19-18:03
INSTRUCTIONS:   小工具url
"""

from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^captcha/', include("extract_apps.rest_captcha.urls"))
]