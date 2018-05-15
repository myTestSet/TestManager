# -*- coding:utf-8 -*-
# @Author= 'liuzunrui'
# @Time :2018/5/15 下午2:25

from django.conf.urls import url

from app.test_util import views

urlpatterns = [
    url(r'^id/$', views.create_id_no, name='create_id'),
]