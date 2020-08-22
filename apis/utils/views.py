from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from extract_apps.rest_captcha.serializers import RestCaptchaSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from main.settings import SECRET_KEY, ACCESS_KEY, BUCKET_NAME

from .serializers import *
from .utils.qiniu_utils import q, put_file


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
            tokens = []
            for i in serializer.validated_data['name']:
                token = q.upload_token(BUCKET_NAME, i, 3600)
                tokens.append(token)
            # ret, info = put_file(token, "不知火.jpg", '/Users/ruler/Pictures/pap.er/妖刀.jpg')
            # print(info)
            data = {
                "token": tokens
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

