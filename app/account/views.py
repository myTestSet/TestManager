# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import authenticate

from models import User
from backend import do_login, update_userinfo_session_cookie


def register(request):
    '''
    注册
    :param request:
    :return:
    '''

    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        department = request.POST['department']
        account = User.objects.create(
            email=email,
            username=username,
            department=department,
        )
        account.set_password(password)
        account.save()
        return redirect('login.html')


def login(request):
    '''
    登录
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        do_login(request, user)
        response = render(request, 'home.html')
        update_userinfo_session_cookie(request, response, user)
        return response