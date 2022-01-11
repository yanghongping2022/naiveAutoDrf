from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# 项目model
class Product(models.Model):
    name = models.CharField(help_text='项目名称', max_length=32)
    desc = models.CharField(help_text='项目描述', max_length=256)
    create_at = models.DateTimeField(help_text='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(help_text='更新时间', auto_now=True)
    creator = models.ForeignKey(help_text='创建者', to=User, to_field='id', on_delete=models.CASCADE)
    maintainer = models.ManyToManyField(help_text='维护者/成员', to=User, related_name='ProductMaintainer',blank=True)
    isActive = models.BooleanField(help_text='是否激活', default=True)

    # db_table自定义数据表名
    class Meta:
        db_table = 'product'


# 项目环境model
class Env(models.Model):
    name = models.CharField(help_text='环境名称', max_length=32)
    desc = models.CharField(help_text='环境描述', max_length=256)
    address = models.CharField(help_text='环境地址', max_length=64)
    create_at = models.DateTimeField(help_text='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(help_text='更新时间', auto_now=True)
    creator = models.ForeignKey(help_text='创建者', to=User, to_field='id', on_delete=models.CASCADE)
    isActive = models.BooleanField(help_text='是否激活', default=True)
    FK_pro = models.ForeignKey(help_text="关联项目", to=Product, to_field='id', on_delete=models.CASCADE)

    # db_table自定义数据表名
    class Meta:
        db_table = 'env_pro'
