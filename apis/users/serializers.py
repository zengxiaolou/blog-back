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
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户信息"""
    id = serializers.IntegerField(read_only=True)
    sms = serializers.CharField(max_length=6, min_length=6, required=True, write_only=True)
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)
    password = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)
    username = serializers.CharField(max_length=20, min_length=3, required=True)
    is_staff = serializers.BooleanField(read_only=True)
    avatar = serializers.CharField(max_length=150, min_length=10, read_only=True)
    email = serializers.EmailField(required=False)
    nickname = serializers.CharField(required=False)
    is_superuser = serializers.BooleanField(read_only=True)

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
        if attrs.get('sms', ''):
            del attrs['sms']
        return attrs

    class Meta:
        model = User
        fields = ('id', 'username', 'sms', 'mobile', 'password', "is_staff", 'avatar', 'email', 'nickname',
                  'github_info', 'is_superuser')
        depth = 1


class UpdateUserSerializer(serializers.ModelSerializer):
    """更新用户信息"""
    code = serializers.CharField(max_length=6, min_length=6, required=False, write_only=True)
    email = serializers.EmailField(max_length=30, min_length=5, required=False)
    mobile = serializers.CharField(max_length=11, min_length=11, required=False)
    nickname = serializers.CharField(max_length=8, min_length=1, required=False)
    avatar = serializers.CharField(max_length=300, min_length=10, required=False)
    password = serializers.CharField(max_length=10, min_length=8, write_only=True, required=False)


    @staticmethod
    def validate_password(password):
        """检查password"""
        if re.match("^(?!\d+$)[\da-zA-Z_]+$", password) is None:
            raise serializers.ValidationError('密码不符合要求')
        return password

    def update(self, instance, validated_data):
        """更新数据"""
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
        if validated_data.get('password', ''):
            instance.set_password(validated_data['password'])
        instance.save()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    def validate_mobile(self, mobile):
        """检验手机号是否合规"""
        # 手机号已注册
        if User.objects.filter(mobile=mobile).first():
            res = self.initial_data.get('reset', False)
            if not res:
                raise serializers.ValidationError("手机号已被绑定")

        code = self.initial_data.get('code', '')
        if code:
            init_code = cache.get('sms' + mobile)
            if init_code == 0:
                raise serializers.ValidationError('验证码过期，请重新获取')
            elif init_code != code:
                raise serializers.ValidationError('验证码错误，请重新获取')
            cache.delete('sms' + mobile)
        else:
            raise serializers.ValidationError('请输入短信验证码')

        return mobile

    def validate_email(self, email):
        """检验邮箱是否合规"""
        # 邮箱已被绑定
        if User.objects.filter(email=email).first():
            res = self.initial_data.get('reset', False)
            if not res:
                raise serializers.ValidationError("邮箱已被绑定")

        code = self.initial_data.get('code', '')
        if code:
            init_code = cache.get('email' + email)
            if init_code == 0:
                raise serializers.ValidationError('验证码过期，请重新获取')
            elif init_code != code:
                raise serializers.ValidationError('验证码错误，请重新获取')
            cache.delete('email' + email)
        else:
            raise serializers.ValidationError('请输入邮箱验证码')

        return email

    def validate(self, attrs):
        """删除sms字段"""
        if attrs.get('code', ''):
            del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['nickname', 'mobile', 'password', 'avatar', 'email', 'code']
        depth = 1
