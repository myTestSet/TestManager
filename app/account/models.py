# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utils.models.mixins import BaseTimeModelMixin


# Create your models here.


class User(BaseTimeModelMixin):
    '''
    用户
    '''
    email = models.CharField(max_length=200)  # 邮箱
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    department = models.CharField(max_length=200)

    class Meta:
        db_table = 'account_user'