from datetime import date

from rest_framework import mixins, viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from apis.utils.utils.other import redis_handle
from .serializers import UserSerializer, UpdateUserSerializer
from apis.utils.permissions import IsOwnerOrReadOnly
from main.settings import COUNT_PREFIX

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """用户相关"""
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializer
        else:
            return UpdateUserSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """用户注册"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def perform_create(self, serializer):
        redis_handle.incr(COUNT_PREFIX + "users", amount=1)
        today = date.today()
        redis_handle.hincrby(COUNT_PREFIX + 'user', str(today), amount=1)
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['username'] = user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)