# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
from django.shortcuts import render, redirect, HttpResponse

from backend import get_test_data
from constants import AREA_TYPE, area_code, NAME_FILTER_FLAG, IS_RANDOM
from utils.DbUtils.dbutil import dbutil_select, insert_db

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


def create_activity(request):
    if request.method == 'GET':
        return render(request, "hello")
    elif request.method == 'POST':
        filename = request.POST['filename']
        sheetname = request.POST['sheetname']
        test_data = get_test_data(filename, sheetname)
        activity_code = int(test_data[0][u'活动编号'])
        activity_name = test_data[0][u'活动名称']
        activity_area = area_code[test_data[0][u'活动所属省']]
        type_code = int(str(activity_code)[0:6])
        status = 0
        acticity_desc = ''
        start_time_tmp = datetime.datetime.now()
        start_time = start_time_tmp.strftime('%Y%m%d%H%M%S%f')[0:14]
        end_time_tmp = start_time_tmp + datetime.timedelta(days=+30)
        end_time = end_time_tmp.strftime('%Y%m%d%H%M%S%f')[0:14]
        create_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
        update_time = create_time
        create_people = 'S00000000000150'
        update_people = 'S00000000000150'
        setting_remainder = 99999
        award_max_count = 99999
        area_type = AREA_TYPE[test_data[0][u'活动地区范围']]

        # 查询省码
        region_d1_sql = \
            "select a.REGION_D1 from hx_region a where a.region_name like '%s%%'" \
            % test_data[0][u'活动所属省']
        prov_code = dbutil_select(region_d1_sql)[0]
        # 查询市码
        region_d2_sql = \
            "select a.REGION_D2 from hx_region a where a.region_name like '%s%%' and a.status = 1" \
            % test_data[0][u'活动所属市']
        if test_data[0][u'活动所属市'] == '':
            city_code = ''
        else:
            city_code = dbutil_select(region_d2_sql)[0]

        act_condition = test_data[0][u'活动条件']

        if test_data[0][u'活动条件'] == '':
            act_condition = 0
        else:
            act_condition = int(act_condition)

        total_amount = 9999900
        remainder_amount = 9999900
        setting_count = 99999
        prize_percent = 100
        name_filter_flag = NAME_FILTER_FLAG[test_data[0][u'是否名单过滤']]
        is_random = IS_RANDOM[test_data[0][u'是否随机发放奖励']]
        day_max = ''
        remark = '02'
        insert_sql = "insert into hd_activity VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                     "'%s', " \
                     "'%s', %d, %d, '%s', '%s', '%s', %d, %d, %d, %d, %d, '%s', '%s', '%s', '%s')" \
                     % (activity_code, activity_name, activity_area, type_code, status, acticity_desc, start_time,
                        end_time, create_time, update_time, create_people, update_people, setting_remainder,
                        award_max_count, area_type, prov_code, city_code, act_condition, total_amount, remainder_amount,
                        setting_count, prize_percent, name_filter_flag, is_random, day_max, remark
                        )
        print insert_sql
        # insert_db(insert_sql)

        select_sql = "select * from hd_activity a WHERE a.activity_code ='%s'" \
                     % activity_code
        print select_sql
    return render(request, 'msg: sucess')


def create_activity_award(request):
    pass
