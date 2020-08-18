from django.db import models
from django.contrib.auth.models import AbstractUser
from time import time


class UserProfile(AbstractUser):
    """
    用户信息
    """
    avatar = models.CharField(max_length=300, verbose_name="头像")

    def __str__(self):
        return self.username

