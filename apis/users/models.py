from django.db import models
from django.contrib.auth.models import AbstractUser
from time import time


class UserProfile(AbstractUser):
    """
    用户信息
    """
    avatar = models.CharField(max_length=300, default='https://avatars1.githubusercontent.com/u/71955670?s=40&v=4', verbose_name="头像")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号")
    github = models.CharField(max_length=50, default="未绑定", verbose_name="github账号")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.username

