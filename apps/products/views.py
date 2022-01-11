from django.db.models import Q

# Create your views here.
from rest_framework import viewsets, status

from apps.products.models import Product, Env
from apps.products.serializers import ProductSerializer, EnvProSerializer
from common.BasePagination import BasePageNumberPagination

from common.BaseResponse import BaseResponse
from common.Constant import CODE_REJECT_ERROR, MSG_REJECT_ERROR, CODE_PARAMETER_ERROR, MSG_PARAMETER_ERROR


class ProductViewSet(viewsets.ModelViewSet):
    """
    项目模块管理，包括增删改查操作
    models：Product
    """
    # 指定结果集并设置排序
    queryset = Product.objects.filter(isActive=True).order_by('-pk')
    # 指定序列化的类
    serializer_class = ProductSerializer
    # 指定分页
    pagination_class = BasePageNumberPagination
    # 筛选类
    # filterset_fields = ['name', 'creator', 'maintainer']

    def get(self, request):
        """
        获取项目列表
        如果用户是管理员，则可以默认查看所有项目
        如果用户是普通角色，则只能查看本人创建或者所属的项目
        新增筛选功能
        type:
            1：创建的项目
            2：参与的项目
        name: 项目名称  模糊搜索
        creator_username：创建人，模糊搜索
        20201.12.31:
        如果pagesize传-1,则代表返回所有数据
        """
        # if request.GET.get('type') == '1':
        #     self.queryset = self.queryset.filter(
        #         Q(creator=request.user.id) & Q(isActive=True)).order_by('-id')
        # elif request.GET.get('type') == '2':
        #     self.queryset = self.queryset.filter(
        #         Q(maintainer__exact=request.user.id) & Q(isActive=True)).order_by('-id')
        # elif request.user.is_superuser is False:
        if request.user.is_superuser is False:
                self.queryset = self.queryset.filter(
                    Q(creator=request.user.id) | Q(maintainer__exact=request.user.id) & Q(isActive=True)).order_by('-id')
        if request.GET.get('name'):
            # 模糊查找  项目名称
            self.queryset = self.queryset.filter(name__contains=request.GET.get('name'))
        if request.GET.get('username'):
            # 模糊查找  创建人
            self.queryset = self.queryset.filter(creator__username__contains=request.GET.get('username'))
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return BaseResponse(data=self.get_paginated_response(serializer.data).data)
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data)

    def post(self, request):
        """
        新建项目
        项目名称重复，则拒绝创建
        """
        '''解决maintainer多对多传参方式，需要对maintainer接收到的值二次处理下'''
        if Product.objects.filter(name=request.data.get('name'), isActive=True).exists():
            return BaseResponse(code=CODE_PARAMETER_ERROR, message=MSG_PARAMETER_ERROR, data={'error': '项目名称已存在'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return BaseResponse(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_retrieve(self, request, pk, *args, **kwargs):
        """
        查看项目详情
        如果不是项目创建人或者超级管理员，不可操作
        """
        if Product.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '项目已删除'})
        if request.user != Product.objects.get(id=pk).creator and request.user not in Product.objects.get(
                id=pk).maintainer.all() and request.user.is_superuser is False:
            print(request.user != Product.objects.get(id=pk).creator)
            print(request.user not in Product.objects.get(
                id=pk).maintainer.all())
            print(request.user.is_superuser is False)
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return BaseResponse(data=serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        修改项目
        如果不是项目创建人或者超级管理员，不可操作
        """
        if Product.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '项目已删除'})
        if request.user != Product.objects.get(id=pk).creator and request.user.is_superuser is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return BaseResponse(data=serializer.data)

    def delete(self, request, pk):
        """
        删除项目
        如果不是项目创建人或者超级管理员，不可操作
        """
        if Product.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '项目已删除'})
        if request.user != Product.objects.get(id=pk).creator and request.user.is_superuser is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        instance = self.get_object()
        self.perform_destroy(instance)
        print(instance.isActive)
        return BaseResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.isActive = False
        instance.save()
        # instance.delete()


class EnvProViewSet(viewsets.ModelViewSet):
    """
    项目环境模块管理，包括增删改查操作
    models：Env
    """
    # 指定结果集并设置排序
    queryset = Env.objects.filter(isActive=True).order_by('-pk')
    # 指定序列化的类
    serializer_class = EnvProSerializer
    # 指定分页
    pagination_class = BasePageNumberPagination
    # 筛选类
    filterset_fields = ['name', 'FK_pro', 'creator']

    def get(self, request):
        """
        获取项目环境列表
        如果用户是管理员，则可以默认查看
        不是管理员并且满足以下条件则不能访问：
        不是项目创建者
        不是项目维护者
        项目已删除
        """
        # 如果没有传product则返回异常
        if request.GET.get('FK_pro') is None:  # 如果没有传product则返回异常
            return BaseResponse(code=CODE_PARAMETER_ERROR, message=MSG_PARAMETER_ERROR, data={'error': '缺少参数product'})
        # 如果不是超级管理员并且不是项目的成员，或者项目是删除状态，则不能访问
        if request.user.is_superuser is False and not Product.objects.filter(
                Q(creator=request.user.id) | Q(maintainer__exact=request.user.id) & Q(isActive=True) & Q(
                    id=request.GET.get('product'))).exists():
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '项目不存在或无权限访问'})
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return BaseResponse(data=self.get_paginated_response(serializer.data).data)

        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data)

    def post(self, request):
        """
        新建项目环境
        同一项目下环境名称重复，则拒绝创建
        不是项目成员，不能创建环境
        """
        if request.data.get('FK_pro') is None:  # 如果没有传product则返回异常
            return BaseResponse(code=CODE_PARAMETER_ERROR, message=MSG_PARAMETER_ERROR, data={'error': '缺少参数product'})
        # 环境名称重复，则拒绝创建
        if Env.objects.filter(name=request.data.get('name'), isActive=True,
                              FK_pro=request.data.get('FK_pro')).exists():
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '环境名称已存在'})
        # 是超级管理员并且不是项目的成员，或者项目是删除状态，则不能创建
        if request.user.is_superuser is False and not Product.objects.filter(
                Q(creator=request.user.id) | Q(maintainer__exact=request.user.id) & Q(isActive=True) & Q(
                    id=request.GET.get('product'))).exists():
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '项目不存在或无权限访问'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return BaseResponse(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_retrieve(self, request, pk, *args, **kwargs):
        """
        查看项目环境详情
        如果不是项目创建人或者维护者或者超级管理员，不可操作
        """
        if Env.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '环境已删除'})
        if request.user != Env.objects.get(id=pk).FK_pro.creator or request.user not in Env.objects.get(
                id=pk).FK_pro.maintainer.all() or request.user.is_superuser is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return BaseResponse(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        修改项目环境
        如果不是项目创建人或者维护者或者超级管理员，不可操作
        """
        if Env.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '环境已删除'})
        if request.user != Env.objects.get(id=pk).FK_pro.creator or request.user not in Env.objects.get(
                id=pk).FK_pro.maintainer.all() or request.user.is_superuser is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return BaseResponse(data=serializer.data)

    def delete(self, request, pk):
        """
        删除环境
        如果不是项目环境创建人或者超级管理员，不可操作
        """
        if Env.objects.get(id=pk).isActive is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '环境已删除'})
        if request.user != Env.objects.get(id=pk).FK_pro.creator and request.user not in Env.objects.get(
                id=pk).FK_pro.maintainer.all() and request.user.is_superuser is False:
            return BaseResponse(code=CODE_REJECT_ERROR, message=MSG_REJECT_ERROR, data={'error': '没有权限'})
        instance = self.get_object()
        self.perform_destroy(instance)
        return BaseResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.isActive = False
        instance.save()
        # instance.delete()
