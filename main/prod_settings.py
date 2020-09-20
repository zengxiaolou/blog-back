"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/9/20-11:22
INSTRUCTIONS:   生产环境设置
"""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'xiaolou',
        'PASSWORD': 'zzxxyy',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4',
                    # 'init_command': 'SET storage_engine=INNODB;'
                    }
    }
}


# drf_yasg URL配置
YASG_URL = 'http://www.messstack.com/'