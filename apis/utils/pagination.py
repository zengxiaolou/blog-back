"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/30-23:20
INSTRUCTIONS:   分页设计
"""

from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    """自定义分页"""
    page_query_param = 'page'
    page_size_query_param = 'size'
