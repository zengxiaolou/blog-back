"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/10/21-23:06
INSTRUCTIONS:   文件简介
"""

from django.conf.urls import url

from apis.my_statistics.views import StatisticsView

urlpatterns = [
    url(r"^base/$", StatisticsView.as_view())
]