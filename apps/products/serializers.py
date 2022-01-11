from rest_framework import serializers
from .models import Product, Env


class ProductSerializer(serializers.ModelSerializer):
    # 获取当前用户,自动赋值
    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    creator_username = serializers.SerializerMethodField(read_only=True)
    # 格式化时间
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Product  # 指定的模型类
        fields = '__all__'  # 需要序列化的属性

    def get_creator_username(self,obj):
        return obj.creator.username


class EnvProSerializer(serializers.ModelSerializer):
    # 获取当前用户,自动赋值
    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    creator_username = serializers.SerializerMethodField(read_only=True)
    # 格式化时间
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Env  # 指定的模型类
        fields = '__all__'  # 需要序列化的属性

    def get_creator_username(self,obj):
        return obj.creator.username