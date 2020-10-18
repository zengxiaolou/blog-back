from rest_framework import status, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apis.utils.utils.other import generate_code
from extract_apps.rest_captcha.serializers import RestCaptchaSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from main.settings import QINIU_BUCKET_NAME

from apis.utils import tasks

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
            token = q.upload_token(QINIU_BUCKET_NAME, serializer.validated_data['name'], 3600)
            data = {
                "token": token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailView(APIView):
    """生成email 验证码并发送"""
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(request_body=EmailSerializer, responses={201: EmailSerializer})
    def post(self, request, *args, **kwargs):
        res = request.data.get('reset', '')
        if res:
            serializer = ResetEmailSerializer(data=request.data)
        else:
            serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = generate_code()
            res = tasks.send_mails.delay('www.messstack.com', code, email)
            cache.set('email' + email, code, 300)
            return Response({"data": "邮件已发送", "task_id": res.task_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """手机短信"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        code = generate_code()
        tasks.send_sms.delay(mobile=mobile, code=code)
        cache.set('sms' + mobile, code, 300)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VerifyView(APIView):
    """验证验证码是否正确"""

    @swagger_auto_schema(request_body=VerifySerializer, responses={200: VerifySerializer})
    def post(self, request, *args, **kwargs):
        request.data['id'] = request.user.id
        serializer = VerifySerializer
        if serializer.is_valid():
            cache.set('verify' + request.user.id, 1, 600)
            return Response({'result': '身份验证通过，可以继续下一步操作'}, status=status.HTTP_200_OK)
        return Response({'result': '身份验证失败'}, status=status.HTTP_400_BAD_REQUEST)
