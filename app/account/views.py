# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import transaction

# Create your views here.

from models import User


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        department = request.POST['department']
        try:
            with transaction.atomic():
                account = User.objects.create(
                    email=email,
                    username=username,
                    department=department
                )
                account.set_password(password)
                account.save()
                return render(request, 'login.html')
        except:
            return render(request, "")
    elif request.method == 'GET':
        return render(request, 'register.html')
