from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model

from .serializers import LikeSerializer
from apis.article.models import Article

user = get_user_model()


class LikeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """点赞相关"""
    queryset = user.objects.all()
    serializer_class = LikeSerializer

