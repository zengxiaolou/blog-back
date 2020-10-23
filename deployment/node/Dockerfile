# 建立python3.3环境
FROM node

# 镜像作者
MAINTAINER zxy Zengevent@gmail.com

# 设置python 环境变量
ENV PYTHONUNBUDFFERED 1
ENV APP_ENV "docker"

# 创建project 文件夹
RUN mkdir /work

# 将project文件夹设为工作路径
WORKDIR /work

# 将当前目录加入到工作路径
ADD . /work

# 安装相关依赖
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN cnpm install pm2 -g
RUN cnpm install -g express
RUN cnpm install -g phantomjs-prebuilt

# 设置环境变量
ENV SPIDER=/work