# -*- coding:utf-8 -*-
from django.conf.urls import url
import views
__author__ = 'liuzunrui'


urlpatterns = [
    url(r'upload-file.html$', views.upload_file, name='upload_file'),
    url(r'file-list.html$', views.file_list, name='file_list'),
    url(r'create-activity$', views.create_activity, name='create_activity'),
    url(r'create-activity-award$', views.create_activity_award, name='create_activity_award'),
    url(r'create-lottery$', views.create_lottery, name='create_lottery'),
    url(r'create-lottery-award$', views.create_lottery_award, name='create_lottery_award'),
]
