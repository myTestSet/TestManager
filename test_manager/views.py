# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Project
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def add_project(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        user_name = request.POST['user_name']
        Project.objects.create(project_name=project_name, user_name=user_name)
        return redirect('project_list/')
    return render(request, 'add-project.html')


def project_list(request):
    projects = Project.objects.all()
    project_lists = [project for project in projects]
    print project_lists
    contexts = {'project_lists': project_lists}
    return render(request, 'project-list.html', contexts)
