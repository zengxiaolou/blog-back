from django.db import models
from django.contrib.auth.models import AbstractUser
from time import time


class UserProfile(AbstractUser):
    """
    用户信息
    """
