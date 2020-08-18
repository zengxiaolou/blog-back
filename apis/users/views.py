from rest_framework import mixins, viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import jwt_decode_handler, jwt_payload_handler

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):
    """用户相关"""
    queryset = User.objects.all()
    serializers_class = UserSerializer()

