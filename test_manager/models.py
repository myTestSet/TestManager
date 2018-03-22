# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BaseModel(models.Model):
    '''
    基础 model
    '''
    create_time = models.DateTimeField(auto_created=True, auto_now=True)
    update_time = models.DateTimeField(auto_now=True)


class Project(BaseModel):
    '''
    项目
    '''
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'pro_project'


class Suite(BaseModel):
    '''
    测试用例集
    集合相关 所有的 testcase，
    主要用来存储全局配置
    '''
    suite_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # 测试用例集名称

    variables = models.CharField(max_length=1024, blank=True, null=True)
    parameters = models.CharField(max_length=1024, blank=True, null=True)
    # 公共参数，常用参数为基础 url，
    request = models.CharField(max_length=1024, blank=True, null=True)
    project_id = models.ForeignKey(Project, blank=True, null=True)

    class Meta:
        db_table = 'test_suite'


class Case(BaseModel):
    '''
    用例
    '''
    suite_id = models.ForeignKey(Suite, blank=True, null=True)
    case_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # 用例名称

    # 测试用例中定义的变量
    variables = models.CharField(max_length=500, blank=True, null=True)

    # 测试用例中定义的参数列表，作用域为当前测试用例，用于实现对当前测试用例进行数据化驱动
    parameters = models.CharField(max_length=1024, blank=True, null=True)

    # HTTP请求的详细内容，包括 url 路径，请求方法，数据,具体可参考
    # http://docs.python-requests.org/en/master/api/#requests.Request
    request = models.TextField(default=None)

    # 从当前 HTTP 请求的响应结果中提取参数，并保存到参数变量中（例如token），后续测试用例可通过$token的形式进行引用
    extract = models.CharField(max_length=500, blank=True, null=True)

    # 测试用例中定义的结果校验项，作用域为当前测试用例，用于实现对当前测试用例运行结果的校验
    validate = models.CharField(max_length=500, default=None)
    is_del = models.IntegerField(default=0)

    class Meta:
        db_table = 'api_case'
