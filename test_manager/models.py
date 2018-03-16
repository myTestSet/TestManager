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
    项目名称
    '''
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'pro_project'


class Case(BaseModel):
    case_id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=100)
    
