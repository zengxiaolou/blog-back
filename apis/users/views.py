from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """用户相关"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

