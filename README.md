# Introduction

- 该项目是各简单的blog，通过前后端分离的方式编写
- 前端：
  - 框架：Vue
  - 脚手架：Vue-cli4
  - 组件：Vuex、Vue-router、Axios
  - 第三方组件：Echarts、 ToastUI-Editor
  - UI库：ElementUI
  - 具体信息请查看 [前端项目](https://github.com/zengxiaolou/blog-front/)
- 后端：
  - 语言：Python3.7
  - 框架：Django、 Django-Restful-Framework
  - 主要插件：Social、Jwt、Celery、Sentry、drf_yasg
  - 数据库：Redis、Mysql、ElasticSearch
  - 部署：使用Docker-compose 容器编排可以快速自动部署、Nginx

# Deploy

## 部署前置操作：
- docker: [教程地址](https://www.runoob.com/docker/ubuntu-docker-install.html)
- docker-compose: `pip/pip3 install docker-compose`
- git: apt/yum install git

## 账号配置
由于项目中涉及到短信、邮件、OSS服务、第三方登录等私人账号密钥，需要自行配置，配置文件路径为
/blog-back/main/keys_example.py 具体配置根据注释填写。配置完成后，将文件名改为keys.py
即可。其余配置可在/blog-back/main/setting.py与/blog-back/main/docker_setting.py
中配置。

## 开发环境配置
基础同上，开发环境需自行安装mysql、elasticsearch、redis与python相关依赖
python相关依赖可通过 在项目根路径下执行 `pip install -r requirement.txt`完成安装

## 服务器部署

```
# 选择合适的目录，拉取项目代码（个人推荐将项目代码放到/opt目录下）
cd /opt
# 拉取项目代码 （前端文件已挂载到后端项目中）
`git clone https://github.com/zengxiaolou/blog-back.git` 
# 进入项目
cd /blog-back
# 执行部署命令
docker-compose up --build 
# 首次部署需要build项目代码，后续启动项目使用/后台启动 想进一步了解docker，请自行学习
docker-compose up ｜｜ docker-compose up -d
```

## 项目文件目录说明
目前项目目录仍比较乱，后续有时间将优化调整目录结构，使之清晰易理解
```
├── Dockerfile  项目docker 打包成镜像文件
├── README.md   项目介绍
├── apis        接口apps （由于采用restful接口规范，该文件夹下均只提供数据，不做页面渲染）
│   ├── __init__.py
│   ├── article     文章相关视图
│   │   ├── __init__.py
│   │   ├── admin.py    
│   │   ├── apps.py
│   │   ├── documents.py    es文档序列化（由于项目采用es作为全文搜索数据库，即检索需要通过该文件做序列化）
│   │   ├── filters.py      过滤器
│   │   ├── migrations      ORM映射
│   │   │   └── __init__.py
│   │   ├── models.py       数据库关系映射相关类
│   │   ├── serialzers.py   model系列化
│   │   ├── tasks.py        定时任务
│   │   ├── tests.py        
│   │   ├── urls.py         router/路由相关
│   │   ├── utils.py        小工具
│   │   └── views.py        视图
│   ├── my_statistics       网站各项统计视图（各文件功能同上）
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── operations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── users   用户信息相关（注册、登录、获取/修改信息）
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   └── utils       各类小工具（短信、邮箱、图形验证码）
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   └── __init__.py
│       ├── models.py
│       ├── pagination.py   分页设置
│       ├── permissions.py  权限设置
│       ├── serializers.py
│       ├── tasks.py
│       ├── tests.py
│       ├── urls.py
│       ├── utils
│       │   ├── __init__.py
│       │   ├── other.py
│       │   └── qiniu_utils.py
│       └── views.py
├── celerybeat-schedule.db
├── deployment      docker部署相关文件
│   ├── mysql   msyql数据库
│   │   └── conf   mysql配置
│   │       └── my.cnf
│   ├── nginx   
│   │   ├── Dockerfile  镜像构建文件
│   │   ├── conf    
│   │   │   └── nginx.conf http相关配置
│   │   └── nginx.conf  server配置
│   └── node    优化seo文件采用旁路机制，通过爬虫在服务端渲染，以提高blog被检索到的概率
│       ├── Dockerfile
│       ├── README.md
│       ├── package.json
│       ├── server.js
│       └── spider.js
├── dist    前端文件挂载目录
├── docker-compose.yml  docker编排文件，用于编排各项服务（nginx、redis、es、blog_web、mysql）的docker文件
├── extract_apps  其他第三方app、由于直接import 该app无法满足需求，故修改部分代码，需和项目打包
│   ├── __init__.py
│   ├── rest_captcha    图形验证码app
│   └── social_core     第三方登录 app
├── gunicorn.conf   独角兽配置文件，具体请自行百度
├── init.sh 初始化文件脚本
├── main    
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py   异步调度配置文件
│   ├── dev_settings.py     开发环境配置文件
│   ├── docker_settings.py  docker自动化部署配置文件
│   ├── prod_settings.py    自行单独部署配置文件
│   ├── settings.py     公用基础配置文件
│   ├── urls.py     主路由入口文件
│   └── wsgi.py
├── manage.py       
├── requirement.txt     python项目依赖
├── start.sh        项目启动脚本
└── static      项目依赖静态文件
```