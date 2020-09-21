"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/20-11:29
INSTRUCTIONS:   docker部署环境配置
"""
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'xiaolou',
        'PASSWORD': 'zzxxyy',
        'HOST': 'db',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4',
                    # 'init_command': 'SET storage_engine=INNODB;'
                    }
    }
}

# drf_yasg URL配置
YASG_URL = 'http://www.messstack.com/'

# 内存设置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}

# broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://redis:6379/1'
# backend配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'es:9200'
    },
}