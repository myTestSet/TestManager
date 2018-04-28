# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def upload_file(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'upload-file.html')
    elif request.method == 'POST':
        myFile = request.FILES.get('myfile')
        print myFile
        if not myFile:
            return render(request, u'没有文件上传')
        destination = open(os.path.join('filedata', myFile.name), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

        return redirect('file-list.html')


def file_list(request):
    split_file_list = []
    file_lists = os.listdir('./filedata')[::-1]
    for i in range(0, len(file_lists), 10):
        split_file_list.append(file_lists[i:i+10])
    list_data = {
        'total': len(file_lists),
        'lists': file_lists,
    }
    return render(request, 'file-list.html', list_data)




#def reports_list(request):
    # split_report_list = []
    # reports_list = os.listdir("./reports")[::-1]
    # for i in range(0, len(reports_list), 10):
    #     split_report_list.append(reports_list[i:i+10])
    # # index = int(request.GET['index'])-1
    # list_data = {
    #     'total': len(reports_list),
    #     'lists': reports_list,
    #     # 'list': split_report_list[index],
    # }
    # return render(request, 'report-list.html', list_data)

