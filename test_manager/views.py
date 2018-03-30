# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from django.shortcuts import render, redirect
from django.forms import model_to_dict
from .models import Project, Suite, Case
from django.http import HttpResponseRedirect, HttpResponse

from httprunner.cli import main_ate
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
    contexts = {
        'total': len(project_lists),
        'project_lists': project_lists
    }
    return render(request, 'project-list.html', contexts)


def edit_project(request):
    if request.method == 'GET':
        return render(request, 'edit-project.html')
    elif request.method == 'POST':
        pid = request.GET.get('pid')  # 获取前端传来的项目 id 值
        project_name = request.POST['project_name']
        user_name = request.POST['user_name']
        Project.objects.filter(project_id=pid).update(
            project_name=project_name,
            user_name=user_name
        )
        return redirect('project-list.html')


def del_project(request):
    pid = request.GET.get('pid')
    Project.objects.filter(project_id=pid).delete()
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
        # parameters = request.POST['parameters']
        request = request.POST['request']
        Suite.objects.create(
            project_id=project_id,
            name=name,
            variables=variables,
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
        'total': len(suite_lists),
        'suite_lists': suite_lists,
    }
    return render(request, 'suite-list.html', contexts)


def edit_suite(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        project_lists = [project for project in projects]
        contexts = {'project_lists': project_lists}
        return render(request, 'edit-suite.html', contexts)
    elif request.method == 'POST':
        sid = request.GET.get('sid')
        project_id = Project.objects.get(pk=request.POST['project_id'])
        name = request.POST['suite_name']
        variables = request.POST['variables']
        # parameters = request.POST['parameters']
        request = request.POST['request']
        Suite.objects.filter(suite_id=sid).update(
            project_id=project_id,
            name=name,
            variables=variables,
            request=request
        )
        return redirect('suite-list.html')


def del_suite(request):
    sid = request.GET.get('sid')
    Suite.objects.filter(suite_id=sid).delete()
    return redirect('suite-list.html')


def add_case(request):
    if request.method == 'GET':
        # projects = Project.objects.all()
        # project_lists = [project for project in projects]
        suites = Suite.objects.all()
        suite_lists = [suite for suite in suites]
        print suite_lists
        contexts = {
            'suite_lists': suite_lists,
        }
        return render(request, 'add-case.html', contexts)
    elif request.method == 'POST':
        name = request.POST['case_name']
        suite_id = Suite.objects.get(pk=request.POST['suite_id'])
        variables = request.POST['variables']
        extract = request.POST['extract']
        validate = request.POST['validate']
        request = request.POST['request']
        Case.objects.create(
            name=name,
            suite_id=suite_id,
            variables=variables,
            request=request,
            extract=extract,
            validate=validate
        )
        return redirect('case-list.html')


def case_list(request):
    cases = Case.objects.all()
    case_lists = [case for case in cases]
    contexts = {
        'total': len(case_lists),
        'case_lists': case_lists
    }
    return render(request, 'case-list.html', contexts)


def edit_case(request):
    if request.method == 'GET':
        suites = Suite.objects.all()
        suite_lists = [suite for suite in suites]
        contexts = {
            'suite_lists': suite_lists
        }
        return render(request, 'edit-case.html', contexts)
    elif request.method == 'POST':
        cid = request.GET['cid']
        name = request.POST['case_name']
        suite_id = Suite.objects.get(pk=request.POST['suite_id'])
        variables = request.POST['variables']
        extract = request.POST['extract']
        validate = request.POST['validate']
        request = request.POST['request']
        Case.objects.filter(case_id=cid).update(
            name=name,
            suite_id=suite_id,
            variables=variables,
            request=request,
            extract=extract,
            validate=validate
        )
        return redirect('case-list.html')


def runTest(request):
    '''
    已测试集的形式运行测试用例
    :param request:
    :return:
    '''
    if request.method == 'POST':
        sid = request.GET['sid']
        suites = list(Suite.objects.filter(suite_id=sid).values('suite_id'))
        testsets = []
        '''
        处理 suite 中的config
        '''
        for suite_id in suites:
            testset = {}
            testcases = {'testcases': []}
            config = {}
            suite = Suite.objects.get(suite_id=suite_id['suite_id'])
            suite = model_to_dict(suite)
            suite.pop('basemodel_ptr')
            suite.pop('id')
            suite.pop('suite_id')
            suite.pop('project_id')
            for k, v in suite.items():
                if v == '' or v is None:
                    suite.pop(k)
                else:
                    try:
                        suite[k] = eval(v)
                    except:
                        suite[k] = v
            config['config'] = suite
            '''
            根据 suite_id查询所包含的 case'''
            cases = Case.objects.filter(suite_id=suite_id['suite_id'], is_del=0).values()
            for case in cases:
                case.pop('case_id')
                case.pop('update_time')
                case.pop('create_time')
                case.pop('id')
                case.pop('basemodel_ptr_id')
                case.pop('suite_id_id')
                case.pop('is_del')
                for k, v in case.items():
                    if v == '' or v is None:
                        case.pop(k)
                    else:
                        try:
                            case[k] = eval(v)
                        except:
                            case[k] = v
                testcases['testcases'].append(case)
            testset.update(config)
            testset.update(testcases)
            testsets.append(testset)
    # print "++++++++++++++++"
    # print testsets
    # print "+++++++++++++++++"
    # with open('tem.json', 'w') as f:
    #     json.dump(testsets)
    # testsets = 'demo.json'
    # print type(testsets)
    # main_ate(datafilejian)
#     testsets = [
#   {
#     "config": {
#       "headers": {
#         "User-Agent": "HisunPay/3.4.5.7 (iPhone; iOS 9.3.4; Scale/3.00)"
#       },
#       "variables": [],
#       "name": "testset description"
#     }
#   },
#
#
#   {
#     "test": {
#       "validate": [
#         {
#           "eq": [
#             "status_code",
#             200
#           ]
#         },
#         {
#           "eq": [
#             "headers.Content-Type",
#             "text/html;charset=UTF-8"
#           ]
#         }
#       ],
#       "request": {
#         "url": "https://192.168.80.79:23401/mobilepay/rest/wallet/queryInfo",
#         "headers": {
#           "Content-Type": "application/x-www-form-urlencoded"
#         },
#         "data": "data={\n  \"data\" : {\n    \"SESSIONID\" : \"38A8AB618C2792ECFE006369B37A38A5kHI1pxymG+YAdrsxMFBZNSfBF0zqGaDMhxTm0m5q9AY=YbFdrw18RvIRlWOcAsrkjw==\"\n  },\n  \"header\" : {\n    \"MOBILETOKEN\" : \"8803215439855512279\",\n    \"MOBILEMODEL\" : \"iPhone7,1\",\n    \"PLAT\" : \"2\",\n    \"CLIENTVERSION\" : \"9.3.4\",\n    \"APPVERSION\" : \"3.4.5.7\",\n    \"SDKVERSION\" : \"1.0\",\n    \"SESSIONID\" : \"38A8AB618C2792ECFE006369B37A38A5kHI1pxymG+YAdrsxMFBZNSfBF0zqGaDMhxTm0m5q9AY=YbFdrw18RvIRlWOcAsrkjw==\"\n  }\n}",
#         "method": "POST"
#       },
#       "name": "/mobilepay/rest/wallet/queryInfo"
#     }
#   }
# ]
    testsets = [{'testcases': [{'name': u'testcase', 'variables': [{'data0': 'data0'}, {'data1': 'data1'}, {'data2': 'data2'}], 'request': {'url': '#/apitest/caselist/4', 'data': 'request_data', 'method': 'POST'}, 'validate': [{'check': 'compare0', 'comparator': 'eq', 'expect': 0}, {'check': 'compare1', 'comparator': 'eq', 'expect': 1}], 'extract': [{'exract0': 'msg0'}, {'exract1': 'msg1'}]}, {'name': u'data', 'variables': [{'123': 123}], 'request': {'url': 'http://localhost:3000/#/apitest/caselist/4', 'data': '\xe8\xaf\xb7\xe6\xb1\x82\xe6\x95\xb0\xe6\x8d\xae', 'method': 'POST'}, 'validate': [{'check': 1, 'comparator': 'eq', 'expect': 200}], 'extract': []}], 'config': {'name': u'liuzunrui\u2014\u2014module', 'variables': [{'data': 'data'}], 'request': {'base_url': 'http://localhost:3000/#/apitest/suitelist/3'}}}]
    main_ate(testsets)
    return redirect('report-list.html')


def reports_list(request):
    split_report_list = []
    reports_list = os.listdir("./reports")[::-1]
    for i in range(0, len(reports_list), 10):
        split_report_list.append(reports_list[i:i+10])
    # index = int(request.GET['index'])-1
    list_data = {
        'total': len(reports_list),
        'lists': reports_list,
        # 'list': split_report_list[index],
    }
    return render(request, 'report-list.html', list_data)


def get_report(request):
    '''查看报告'''
    report_name = request.GET['reportName']
    return render(request, report_name+"/name.html")