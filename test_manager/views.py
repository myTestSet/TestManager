# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Project, Suite
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
        Project.objects.create(
            project_name=project_name,
            user_name=user_name
        )
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
        Project.objects.filter(id=pid).update(
            project_name=project_name,
            user_name=user_name
        )
        return redirect('project-list.html')


def del_project(request):
    pid = request.GET.get('pid')
    Project.objects.filter(id=pid).delete()
    return redirect('project-list.html')


def add_suite(request):
    '''
    添加模块
    :param request:
    :return:
    '''
    if request.method == 'GET':
        projects = Project.objects.all()
        project_lists = [project for project in projects]
        contexts = {'project_lists': project_lists}
        return render(request, 'add-suite.html', contexts)
    elif request.method == 'POST':
        project_id = Project.objects.get(pk=request.POST['project_id'])  # 外键
        name = request.POST['suite_name']
        variables = request.POST['variables']
        parameters = request.POST['parameters']
        request = request.POST['request']
        Suite.objects.create(
            project_id=project_id,
            name=name,
            variables=variables,
            parameters=parameters,
            request=request
        )
        return redirect('suite-list.html')


def suite_list(request):
    '''
    测试集列表
    '''
    suites = Suite.objects.all()
    suite_lists = [suite for suite in suites]
    contexts = {
        'suite_lists': suite_lists
    }
    return render(request, 'suite-list.html', contexts)


def add_case(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        project_lists = [project for project in projects]
        contexts = {'project_lists': project_lists}
        return render(request, 'add-case.html', contexts)
    elif request.method == 'POST':
        name = request.POST['case_name']


