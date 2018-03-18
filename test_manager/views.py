# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Project
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
'''
修改数据库的不加/
不修改数据的库的加/
'''


def home(request):
    return render(request, 'home.html')


def add_project(request):
    if request.method == 'GET':
        return render(request, 'add-project.html')
    elif request.method == 'POST':
        project_name = request.POST['project_name']
        user_name = request.POST['user_name']
        Project.objects.create(project_name=project_name, user_name=user_name)
        return redirect('project-list.html')


def project_list(request):
    projects = Project.objects.all()
    project_lists = [project for project in projects]
    contexts = {'project_lists': project_lists}
    return render(request, 'project-list.html', contexts)


def edit_project(request):
    if request.method == 'GET':
        return render(request, 'edit-project.html')
    elif request.method == 'POST':
        pid = request.GET.get('pid')  # 获取前端传来的项目 id 值
        project_name = request.POST['project_name']
        user_name = request.POST['user_name']
        Project.objects.filter(id=pid).update(project_name=project_name, user_name=user_name)
        return redirect('project-list.html')


def del_project(request):
    pid = request.GET.get('pid')
    Project.objects.filter(id=pid).delete()
    return redirect('project-list.html')


def add_case(request):
    if request.method == 'GET':
        return render(request, 'add-case.html')
    elif request.method == 'POST':

