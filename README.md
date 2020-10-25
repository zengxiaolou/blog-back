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
## 部署

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


