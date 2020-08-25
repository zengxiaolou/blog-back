"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/25-15:29
INSTRUCTIONS:   文件简介
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry


@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender.__meta.app_label
    model_name = sender.__meta.model_name
    instance = kwargs['instance']

    if app_label == 'article':
        if model_name == 'article':
            instances = instance.article.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender.__meta.app_label
    model_name = sender.__meta.model_name
    instance = kwargs['instance']

    if app_label == 'article':
        if model_name == 'article':
            instances = instance.article.all()
            for _instance in instances:
                registry.update(_instance)