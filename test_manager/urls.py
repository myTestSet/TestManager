# -*- coding:utf-8 -*-

from django.conf.urls import url
from test_manager import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^add-project.html$', views.add_project, name='add_project'),
    url(r'^project-list.html$', views.project_list, name='project_list'),
    url(r'^edit-project.html$', views.edit_project, name='edit_project'),
    url(r'^delete-project.html$', views.del_project, name='del_project'),
    url(r'^add-case.html$', views.add_case, name='add_case'),
]
