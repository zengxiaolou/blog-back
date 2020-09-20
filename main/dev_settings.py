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
YASG_URL = 'http://0.0.0.0:8001/'
