# nginx 镜像
FROM nginx

# 删除原有配置文件，创建金泰文件夹与ssl证书保存文件夹
RUN 
mkdir -p /usr/share/nginx/html/static\
&& mkdir -p /usr/share/nginx/html/media\
&& mkdir -p /usr/share/nginx/ssl

# 添加配置文件
ADD ./nginx.conf /etc/nginx/conf.d/