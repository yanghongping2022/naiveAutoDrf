from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets

from apps.users import serializers
from common.BaseResponse import BaseResponse
from apps.products.models import Product


class LoginAPIView(viewsets.ModelViewSet):
    """
    用户登录获取token
    Args:
        username: 用户名
        password: 密码
    Returns：
        返回一个字典格式的数据
        {'code':int,
        'message':xxx,
        'username':xxx,
        'token':xxx}
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.LoginModelSerializer

    def post(self, request, *args, **kwargs):
        user_ser = self.get_serializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        return BaseResponse(data={
            'id': user_ser.content.get('user').id,
            'username': user_ser.content.get('user').username,
            'is_superuser': user_ser.content.get('user').is_superuser,
            'token': user_ser.content.get('token'),
        })


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理，包括增删改查操作
    models：user
    """
    # 指定结果集并设置排序
    queryset = User.objects.all().order_by('id')
    # 指定序列化的类
    serializer_class = serializers.UserSerializer
    # 筛选类
    filterset_fields = ['username', 'id']


    def get(self, request):
        """
        获取用户列表
        """
        if 'product' in request.GET:
            self.queryset = User.objects.filter(
                id=Product.objects.get(id=request.GET.get('product')).creator.id).order_by('-id') | User.objects.filter(
                id__in=Product.objects.get(id=request.GET.get('product')).maintainer.all()).order_by('id')
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data)
