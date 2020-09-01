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
from django_elasticsearch_dsl.registries import registry

from .models import Article, Category, Tags
from apis.users.models import UserProfile

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAME[__name__])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@registry.register_document
class ArticleDocument(Document):
    # id = fields.IntegerField(attr='id')
    # title = fields.TextField()
    # cover = fields.TextField()
    # summary = fields.TextField()
    # content = fields.TextField()
    # str_num = fields.IntegerField()
    # created = fields.DateField()
    reading_time = fields.IntegerField(attr='reading_time')
    # views_num = fields.IntegerField()
    # comments_num = fields.IntegerField()
    # category = fields.ObjectField(attr='category')
    # tags = fields.TextField(attr='tags')
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
        'id': fields.IntegerField(),
    })
    category = fields.ObjectField(properties={
        'category': fields.TextField(),
        'num': fields.IntegerField(),
    })

    tag = fields.ObjectField(properties={
        'tag': fields.TextField()
    })

    class Index:
        name = 'article'
        settings = {
            "number_of_shards":  1,
            "number_of_replicas": 1
        }

    class Django:
        model = Article
        fields = ['id', 'title', 'cover', 'summary', 'content', 'str_num', 'created', 'views_num', 'comments_num']
        related_models = [UserProfile, Category, Tags]

