from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from extract_apps.rest_captcha.serializers import RestCaptchaSerializer
from drf_yasg.utils import swagger_auto_schema

from .serializers import *


class CheckCaptcha(APIView):
    """检测图形验证码是否正确"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RestCaptchaSerializer

    @swagger_auto_schema(request_body=RestCaptchaSerializer, responses={200: RestCaptchaSerializer})
    def post(self, request, *args, **kwargs):
        serializer = RestCaptchaSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)