"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-17:52
INSTRUCTIONS:   文章搜索
"""
from django.utils import timezone
from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchField, indexes.Indexable):
    """文章搜索"""
    title = indexes.CharField(document=True, model_attr='title')
    summary = indexes.CharField(document=True, model_attr='summary')
    content = indexes.CharField(document=True, use_template=True)

    @staticmethod
    def get_model():
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created__lte=timezone.now()
        )
