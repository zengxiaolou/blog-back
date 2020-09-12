from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from extract_apps.rest_captcha.serializers import RestCaptchaSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from main.settings import BUCKET_NAME

from .serializers import *
from .utils.qiniu_utils import q


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


class GetQiNiuToken(APIView):
    """获取七牛云上传token"""
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=QiNiuUploadSerializer)
    def post(self, request, *args, **kwargs):
        serializer = QiNiuUploadSerializer(data=request.data)
        if serializer.is_valid():
            token = q.upload_token(BUCKET_NAME, serializer.validated_data['name'], 3600)
            data = {
                "token": token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
