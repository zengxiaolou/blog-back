"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/25-14:45
INSTRUCTIONS:   文件简介
"""

from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from .models import Article


INDEX = Index(settings.ELASTICSEARCH_INDEX_NAME[__name__])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@INDEX.doc_type
class ArticleDocument(Document):
    id = fields.IntegerField()
    title = fields.TextField()
    cover = fields.TextField()
    summary = fields.TextField()
    content = fields.TextField()
    created = fields.DateField()
    str_num = fields.IntegerField()
    reading_num = fields.IntegerField()
    views_num = fields.IntegerField()
    comments_num = fields.IntegerField()

    class Django(object):
        model = Article

