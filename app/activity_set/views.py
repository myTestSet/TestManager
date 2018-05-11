# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
from django.shortcuts import render, redirect, HttpResponse

from backend import get_test_data
from constants import AREA_TYPE, area_code, NAME_FILTER_FLAG, IS_RANDOM, AWARD_TYPE, IS_DOUBLE, IS_LOTTERY
from utils.DbUtils.dbutil import dbutil_select, insert_db
from backend import get_award_code, get_lottery_code, get_prize_code
from backend import create_lottery_award_tmp


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
    '''
    创建活动
    :param request:
    :return:
    '''
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
        start_time = (start_time_tmp + datetime.timedelta(minutes=+20)).strftime('%Y%m%d%H%M%S%f')[0:14]
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
    return redirect('upload-file.html')


def create_activity_award(request):
    '''
    活动奖励
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'hello award')
    elif request.method == 'POST':
        filename = request.POST['filename']
        sheetname = request.POST['sheetname']
        test_data = get_test_data(filename=filename, sheetname=sheetname)
        # 抽奖编号：找到当前最大的值 取出后十位，若后十位为9999999999 则抽奖编号为0000000001
        award_code_select = "select MAX(t.award_code) from HD_ACTIVITY_AWARD_SETTING t"
        award_code_tmp = dbutil_select(award_code_select)[0][-10:]
        award_code = get_award_code(award_code_tmp)
        award_name = test_data[0][u'奖励名称']
        award_type = AWARD_TYPE[test_data[0][u'奖励类型']]
        _award_amount = int(test_data[0][u'奖励金额']) * 100
        rule_code_select_sql = "select t.rule_code from HD_WALLET_RULE t WHERE t.total_amount = %d" % _award_amount
        rule_code = dbutil_select(rule_code_select_sql)[0]
        condition_code = test_data[0][u'参与条件']
        is_lottery = IS_LOTTERY[test_data[0][u'是否参与抽奖']]
        award_desc = ''
        award_count = 99999
        remainder = 99999
        per_max_count = test_data[0][u'单人最大奖励份数']
        create_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
        update_time = create_time
        create_people = 'S00000000000150'
        update_people = 'S00000000000150'
        activity_code = int(test_data[0][u'活动编号'])

        reg_real_count = test_data[0][u'特惠数字']  # 互金留存活动中用来作为留存天数的字段
        if reg_real_count == '':
            reg_real_count = 0
        else:
            reg_real_count = int(reg_real_count)
        amt_minimum = int(test_data[0][u'金额下限']) * 100
        amt_maximum = int(test_data[0][u'金额上限']) * 100

        is_double = IS_DOUBLE[test_data[0][u'是否连击翻倍']]
        print is_double
        double_condition_lm = 0
        award_amount = int(test_data[0][u'奖励金额']) * 100
        double_rule_code = test_data[0][u'翻倍条件']

        lottery_num = test_data[0][u'抽奖次数']

        if lottery_num == '':
            lottery_num = 0
        else:
            lottery_num = int(lottery_num)

        insert_award_sql = "insert into HD_ACTIVITY_AWARD_SETTING(" \
                           "AWARD_CODE, AWARD_NAME, AWARD_TYPE,RULE_CODE, CONDITION_CODE, IS_LOTTERY, AWARD_DESC, " \
                           "AWARD_COUNT, REMAINDER, PER_MAX_COUNT, CREATE_TIME, UPDATE_TIME, CREATE_PEOPLE, " \
                           "UPDATE_PEOPLE, ACTIVITY_CODE, REG_REAL_COUNT, AMT_MINIMUN, AMT_MAXIMUN, IS_DOUBLE, " \
                           "DOUBLE_CONDITION_LM, AWARD_AMOUNT, DOUBLE_RULE_CODE, LOTTERY_NUM) " \
                           "VALUES ('%s', '%s', '%s', '%s', '%s', '%s'," \
                           " '%s', %d, %d, %d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d, '%s', %d," \
                           " %d, '%s', %d)" % (award_code, award_name, award_type, rule_code, condition_code,
                                               is_lottery, award_desc, award_count, remainder, per_max_count,
                                               create_time, update_time, create_people, update_people, activity_code,
                                               reg_real_count, amt_minimum, amt_maximum, is_double, double_condition_lm,
                                               award_amount, double_rule_code, lottery_num)

        print insert_award_sql
        # insert_db(insert_award_sql)
    return redirect('upload-file.html')


def create_lottery(request):
    '''
    抽奖设置
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'hello lottery')
    elif request.method == 'POST':
        filename = request.POST['filename']
        sheetname = request.POST['sheetname']
        test_data = get_award_code(filename, sheetname)
        lottery_code_select = "select MAX(t.LOTTERY_CODE) from HD_LOTTERY t"
        lottery_code_tmp = dbutil_select(lottery_code_select)[0][-10:]
        lottery_code = get_lottery_code(lottery_code_tmp)
        lottery_name = test_data[0][u'抽奖名称']
        activity_code = int(test_data[0][u'活动编号'])
        start_time_select_sql = "select t.start_time from hd_activity t where t.activity_code = '%s'" % activity_code
        end_time_select_sql = "select t.end_time from hd_activity t where t.activity_code = '%s'" % activity_code
        start_time = dbutil_select(start_time_select_sql)[0]
        end_time = dbutil_select(end_time_select_sql)[0]
        status = '0'
        create_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
        update_time = create_time
        create_people = 'S00000000000150'
        update_people = 'S00000000000150'
        probablitity_flag = '1'
        insert_lottery_sql = "insert into hd_lottery VALUES (" \
                             "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %\
                             (lottery_code, lottery_name, start_time, end_time, status, activity_code, create_time,
                              update_time, create_people, update_people, probablitity_flag)
        print insert_lottery_sql
        # insert_db(insert_lottery_sql)
    return redirect('upload-file.html')


def create_lottery_award(request):
    '''
    抽奖奖项设置
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'lottery_award')
    elif request.method == 'POST':
        filename = request.POST['filename']
        sheetname = request.POST['sheetname']
        test_data = get_test_data(filename, sheetname)
        prize_code_select = "select MAX(T.prize_code) from HD_LOTTERY_SETTING T"
        prize_code_tmp = dbutil_select(prize_code_select)[0][-10:]
        activity_code = int(test_data[0][u'活动编号'])
        prize_code = get_prize_code(prize_code_tmp)
        lottery_code_sql = "select T.lottery_code from HD_LOTTERY T WHERE T.activity_code = '%s'" % activity_code
        lottery_code = dbutil_select(lottery_code_sql)[0]
        version = 0
        platform_id = '0001'
        create_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
        update_time = create_time
        create_people = 'S00000000000150'
        update_people = 'S00000000000150'
        goods_name = ''
        create_lottery_award_tmp(
            test_data, prize_code,
            lottery_code, create_time,
            update_time, create_people,
            update_people, version,
            goods_name, platform_id
        )

    return render('upload-file.html')
