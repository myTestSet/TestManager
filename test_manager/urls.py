# -*- coding:utf-8 -*-

from django.conf.urls import url
from test_manager import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^add_project$', views.add_project, name='add_project'),
    url(r'^project_list/$', views.project_list, name='project_list'),
]
