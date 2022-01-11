import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class LoginModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=64,
        min_length=3
    )
    password = serializers.CharField(
        max_length=64,
        min_length=3
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    # 在全局钩子中完成token的签发
    def validate(self, attrs):
        # 先从model表中查出user对象
        user = self._validate_user(attrs)
        # 将user对象包装进载荷中
        payload = jwt_payload_handler(user)
        # 将载荷签发入token
        token = jwt_encode_handler(payload)
        # 将对象和token储存进serializer对象中，就可以在视图类中调用
        self.content = {
            'user': user,
            'token': token,
        }
        return attrs

    def _validate_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # 多方式登陆
        if re.match(r'.*@.*', username):
            user = User.objects.filter(email=username).first()
        elif re.match(r'^1[3-9][0-9]{9}$', username):
            user = User.objects.filter(mobile=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({'data': {'error': '用户信息系有误！请重新登录!'}})

        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = User  # 指定的模型类
        fields = '__all__'  # 需要序列化的属性
