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