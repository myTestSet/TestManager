# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.account import views

urlpatterns = [
    url(r'^register.html$', views.register, name='register'),
    url(r'^login.html$', views.login, name='login'),
]
