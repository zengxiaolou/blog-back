"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/20-11:22
INSTRUCTIONS:   生产环境设置
"""

# SECURITY WARNING: don't run with debug turned on in production!
from main.keys import PROD_SQL_KEY

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'xiaolou',
        'PASSWORD': PROD_SQL_KEY,
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4',
                    # 'init_command': 'SET storage_engine=INNODB;'
                    }
    }
}


# drf_yasg URL配置
YASG_URL = 'http://blog.messstack.com/'

# 内存设置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}

# broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
# backend配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

# redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PREFIX = 'article:'
USER_PREFIX = 'user:'
COMMENT_PREFIX = 'comment:'
COUNT_PREFIX = 'count:'