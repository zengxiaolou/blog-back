"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/25-14:45
INSTRUCTIONS:   文件简介
"""

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Article, Category, Tags, ArticleDraft
from apis.users.models import UserProfile


@registry.register_document
class ArticleDocument(Document):
    reading_time = fields.IntegerField(attr='reading_time')
    like_user = fields.ObjectField(properties={
        'username': fields.TextField(),
    })
    category = fields.ObjectField(properties={
        'category': fields.TextField(),
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
        fields = ['id', 'title', 'cover', 'summary', 'content', 'str_num', 'created', 'views_num', 'comments_num',
                  'markdown']
        related_models = [UserProfile, Category, Tags]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(ArticleDocument, self).get_queryset().select_related(
            'category'
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, UserProfile):
            return related_instance.article.all()
        elif isinstance(related_instance, Category):
            return related_instance.article.all()
        elif isinstance(related_instance, Tags):
            return related_instance.article.all()


@registry.register_document
class ArticleDraftDocument(Document):
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
    })
    category = fields.ObjectField(properties={
        'category': fields.TextField(),
    })

    tag = fields.ObjectField(properties={
        'tag': fields.TextField()
    })

    class Index:
        name = 'draft'
        settings = {
            "number_of_shards":  1,
            "number_of_replicas": 1
        }

    class Django:
        model = ArticleDraft
        fields = ['id', 'title', 'cover', 'summary', 'content']
        related_models = [UserProfile, Category, Tags]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(ArticleDraftDocument, self).get_queryset().select_related(
            'user'
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, UserProfile):
            return related_instance.draft.all()
        elif isinstance(related_instance, Category):
            return related_instance.draft.all()
        elif isinstance(related_instance, Tags):
            return related_instance.draft.all()
