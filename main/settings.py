"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import datetime
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


from main.keys import JWT_KEY, KEY_EMAIL_HOST_USER, KEY_EMAIL_HOST_PASSWORD, KEY_QINIU_ACCESS_KEY, \
    KEY_QINIU_SECRET_KEY, KEY_QINIU_BUCKET_NAME, KEY_SOCIAL_AUTH_GITHUB_KEY, KEY_SOCIAL_AUTH_GITHUB_SECRET,\
    TENCENT_SECRETID, TENCENT_SECRETKEY, TENCENT_SMSSDKAPPID, TENCENT_SIGN, TENCENT_TEMPLATEID


APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'prod':
    from .prod_settings import *
elif APP_ENV == 'dev':
    from .dev_settings import *
elif APP_ENV == 'docker':
    from .docker_settings import *
else:
    from .dev_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apis'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extract_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=tpgy423n=fhwr*&k9^tk@_^%%z9gm7m+5%6t*0p2r3zw=%fb1'

ALLOWED_HOSTS = ["*", ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apis.users',
    'apis.utils',
    'apis.article',
    'apis.operations',
    'apis.my_statistics',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'extract_apps.rest_captcha',
    'django_elasticsearch_dsl',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 注意顺序，必须放在这儿
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 允许所有的请求头
CORS_ALLOW_HEADERS = ('*',)
# 允许所有方法
CORS_ALLOW_METHODS = ('*',)

ROOT_URLCONF = 'main.urls'
AUTH_USER_MODEL = 'users.UserProfile'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# 日志设置

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # 格式化
        'simple': {
            'format': '[%(asctime)s] %(filename)s %(lineno)d ==> %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
                },
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(pathname)s %(lineno)d ==> %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
                }
    },
    'handlers': {  # 处理器
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'fileHandler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': 'art.log'
        }

    },
    'loggers': {  # 记录器
        'django_log': {
            'handlers': ['console', 'fileHandler'],
            'level': 'INFO',
            'propagate': False
        }

    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 媒体文件路径
MEDIA_URL = "/media/"

# 媒体文件根路径
MEDIA_ROOT = os.path.join(BASE_DIR, "static/../media")

MEDIAFILES_DIRS = (
    os.path.join(BASE_DIR, "static/../media"),
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    # 版本使用的参数名称
    'VERSION_PARAM': 'version',
    # 默认使用的版本
    'DEFAULT_VERSION': 'v1',
    # 分页设置
    'DEFAULT_PAGINATION_CLASS': 'apis.utils.pagination.MyPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_BULK_OPERATION_HEADER_NAME': None
}


# JWT 配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 生成的token有效期
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apis.users.utils.jwt_response_payload_handler',  # response中token的payload部分处理函数
    'JWT_SECRET_KEY': JWT_KEY,
}

# 手机号正则表达式
REGEX_MOBILE = "^1[354789]\d{9}$|^147\d{8}$|^176\d{8}$"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'  # 发送邮件的服务器地址
EMAIL_HOST_USER = KEY_EMAIL_HOST_USER  # 不含‘@126.com’的后缀
EMAIL_HOST_PASSWORD = KEY_EMAIL_HOST_PASSWORD  # 非邮箱登录密码
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = '小楼的破栈<18328457630@163.com>'

# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# 七牛云设置
# 需要填写你的Access_key 和 Secret_key
QINIU_ACCESS_KEY = KEY_QINIU_ACCESS_KEY
QINIU_SECRET_KEY = KEY_QINIU_SECRET_KEY
QINIU_BUCKET_NAME = KEY_QINIU_BUCKET_NAME


# Elasticsearch configuration
ELASTICSEARCH_INDEX_NAME = {
    'apis.article.documents': "article"
}

USE_X_FORWARDED_HOST = True

# social_setting
AUTHENTICATION_BACKENDS = (
    'apis.users.utils.CustomBackend',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://blog.messstack.com/'
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GITHUB_KEY = KEY_SOCIAL_AUTH_GITHUB_KEY
SOCIAL_AUTH_GITHUB_SECRET = KEY_SOCIAL_AUTH_GITHUB_SECRET


sentry_sdk.init(
    dsn="http://a488b392f75d49f381dd7b2def938b9f@154.91.197.66:9000/2",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)