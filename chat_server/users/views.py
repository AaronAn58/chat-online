import hashlib

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from chat_server.chat_server.serializers import CustomModelSerializer
from chat_server.users.forms import RegistrationForm
from chat_server.users.models import Users
from chat_server.utils.http_response import HttpResponse, HttpCode
from chat_server.utils.viewsets import CustomModelViewSet


# Create your views here.
class LoginNoCaptchaSerializer(CustomModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Users
        field = ['username', 'password']


class LoginNoCaptchaView(APIView):
    serializer_class = LoginNoCaptchaSerializer
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_obj = auth.authenticate(
            request,
            username=username,
            password=hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
        )

        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            return HttpResponse(code=HttpCode.UN_AUTH, msg="账号/密码错误")


class RegisterSerializer(CustomModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = Users
        fields = ["username", "password", "phone"]
        read_only_fields = ["id"]
        write_only_fields = ['password']

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        phone = validated_data.get("phone")
        user_obj = Users.objects.create(
            username=username,
            password=hashlib.md5(password.encode(encoding="utf-8")).hexdigest(),
            phone=phone,
        )
        return user_obj

    def validate(self, attrs):
        username = attrs.get("username")
        if Users.objects.filter(username=username).exists():
            raise APIException("用户名已存在")
        return attrs


class RegisterView(CustomModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = []

    def update(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(code=HttpCode.OK, msg="账户创建成功")
        return HttpResponse(code=HttpCode.PARAMS_ERROR, msg="账户已存在")
