"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/20-11:24
INSTRUCTIONS:   开发环境配置
"""
from .keys import DEV_SQL_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 数据库相关
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': DEV_SQL_KEY,
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4',
                    # 'init_command': 'SET storage_engine=INNODB;'
                    }
    }
}

# drf_yasg URL配置
YASG_URL = 'http://0.0.0.0:8000/'

# 内存设置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        # "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        },
        'KEY_PREFIX': 'article',                                             # 缓存key的前缀（默认空）
        'VERSION': '1',                                                 # 缓存key的版本（默认1）
    }
}

# broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'
# backend配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'

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
