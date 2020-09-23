# 设置最大文件描述
echo "初始化基础配置"
if [ -z "`grep "*		soft		nofile		65536" /etc/security/limits.conf`" ]; then
	echo "*		soft		nofile		65536">>/etc/security/limits.conf
	echo "* 	hard		nofile		65536">>/etc/security/limits.conf
fi

if [ -z "`grep "vm.max_map_count=262144" /etc/sysctl.conf`" ]; then
	echo "vm.max_map_count=262144">>/etc/sysctl.conf
	sysctl -p
fi

# 创建修改es data与logs文件夹权限
currentdir=$(readlink -f "$(dirname '$0')")

es=$currentdir/deployment/es
data_file=$es/data
logs_file=$es/logs

if [  ! -d $es ]; then
	mkdir -p $es



if [ ! -d $data_file ]; then
	mkdir -p $data_file
	chmod 777 -R $data_file 


if [ ! -d $logs_file ]; then
	mkdir -p $logs_file
	chmod 777 -R $logs_file 
