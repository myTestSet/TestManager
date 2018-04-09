# -*- coding:utf-8 -*-

from django.db import models


class BaseTimeModelMixin(models.Model):
    '''
    时间模块，
    主要有创建时间和更新时间
    '''
    create_time = models.DateTimeField(auto_created=True, auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

