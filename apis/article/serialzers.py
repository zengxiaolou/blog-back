"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:03
INSTRUCTIONS:   文章序列化
"""
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ArticleIndex


class ArticleSerializer(HaystackSerializer):

    class Mate:
        index_classes = [ArticleIndex]
        fields = ["title", "summary", "content"]

