from rest_framework import serializers
from django.utils.translation import ugettext as _
from django.core.cache import caches
from .settings import api_settings
from . import utils

cache = caches[api_settings.CAPTCHA_CACHE]


class RestCaptchaSerializer(serializers.Serializer):
    """
    判断验证码是否正确
    """
    captcha_key = serializers.CharField(max_length=64)
    captcha_value = serializers.CharField(max_length=8, trim_whitespace=True)

    def validate(self, data):
        """
        判断验证各项是否满足要求
        :param data: 
        :return: 
        """
        super(RestCaptchaSerializer, self).validate(data)
        cache_key = utils.get_cache_key(data['captcha_key'])
        if data['captcha_key'] in api_settings.MASTER_CAPTCHA:
            real_value = api_settings.MASTER_CAPTCHA[data['captcha_key']]
        else:
            real_value = cache.get(cache_key)

        if real_value is None:
            raise serializers.ValidationError(
                 _('图片验证码过期'))

        cache.delete(cache_key)
        if data['captcha_value'].upper() != real_value:
            raise serializers.ValidationError(_('图片验证码错误'))
        return data
