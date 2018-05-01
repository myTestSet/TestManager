# -*- coding:utf-8 -*-
from django.conf.urls import url
import views
__author__ = 'liuzunrui'


urlpatterns = [
    url(r'upload-file.html$', views.upload_file, name='upload_file'),
    url(r'file-list.html$', views.file_list, name='file_list'),
    url(r'create-activity/$', views.create_activity, name='create_activity'),
]
