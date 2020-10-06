"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/18-13:09
INSTRUCTIONS:   用户信息序列化
"""
import re
from django.core.cache import cache
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
        用户信息
    """
    sms = serializers.CharField(max_length=6, min_length=6, required=True, write_only=True)
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)
    password = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)
    username = serializers.CharField(max_length=20, min_length=3, required=True)

    @staticmethod
    def validate_username(username):
        """检查用户名是否合规"""
        print(username)
        if re.match("^(?!\d+$)[\da-zA-Z_]+$", username) is None:
            raise serializers.ValidationError('用户名不符合要求')
        if User.objects.filter(username=username).first():
            raise serializers.ValidationError('该用户名已存在')
        return username

    @staticmethod
    def validate_password(password):
        """检查password"""
        if re.match("^(?!\d+$)[\da-zA-Z_]+$", password) is None:
            raise serializers.ValidationError('密码不符合要求')
        return password

    def create(self, validated_data):
        user = super(UserSerializer, self).create(
            validated_data=validated_data)  # user对象是Django中继承的AbstractUser
        # UserProfile-->AbstractUser-->AbstractBaseUser中有个set_password(self, raw_password)方法
        user.set_password(validated_data['password'])  # 取出password密码，进行加密后保存
        user.save()
        # ModelSerializer有一个save()方法，save()里面会调用create()函数，这儿重载了create()函数，加入加密的逻辑
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate_mobile(self, mobile):
        """检验手机号是否合规"""
        # 手机号已注册
        if User.objects.filter(mobile=mobile).first():
            res = self.initial_data.get('reset', False)
            if not res:
                raise serializers.ValidationError("手机号已被注册")
        return mobile

    def validate_sms(self, sms):
        """检查sms是否合规"""
        mobile = self.initial_data['mobile']
        init_code = cache.get('sms' + mobile)
        if init_code == 0:
            raise serializers.ValidationError('验证码过期，请重新获取')
        elif init_code != sms:
            raise serializers.ValidationError('验证码错误，请重新获取')
        cache.delete('sms' + mobile)
        return sms

    def validate(self, attrs):
        """删除sms字段"""
        del attrs['sms']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'sms', 'mobile', 'password')


