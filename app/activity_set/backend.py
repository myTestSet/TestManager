# -*- coding:utf-8 -*-

# __author__ = 'liuzunrui'
import datetime
from utils.fileUtil.readfile import ExcelUtil
from utils.DbUtils.dbutil import dbutil_select, insert_db


def get_test_data(filename, sheetname):
    data = ExcelUtil("filedata/" + filename + ".xls", (u'%s' % sheetname))
    print "../filedata/" + filename + ".xls", (u'%s' % sheetname)
    test_data = data.get_data()
    return test_data


def get_award_code(data_tmp):
    '''
    根据规则生成奖励编号
    :param data_tmp:
    :return:
    '''
    if data_tmp == '9999999999':
        _award_code = '0000000001'
    elif data_tmp != '9999999999':
        _award_code = str(int(data_tmp) + 1)
        s_0 = ''
        for i in range(0, 10-len(_award_code)):
            s_0 += '0'
        _award_code = s_0 + _award_code
    _award_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:8] + _award_code
    return _award_code


def get_lottery_code(data_tmp):
    '''
    根据规则生成抽奖编号
    :return:
    '''
    if data_tmp == '9999999999':
        _lottery_code = '0000000001'
    elif data_tmp != '9999999999':
        _lottery_code = str(int(data_tmp) + 1)
        s_0 = ''
        for i in range(0, 10 - len(_lottery_code)):
            s_0 += '0'
        _lottery_code = s_0 + _lottery_code
    _lottery_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:8] + _lottery_code
    return _lottery_code


def get_prize_code(data_tmp):
    '''
    根据规则生成 奖励编号
    :param data_tmp:
    :return:
    '''

    if data_tmp == '9999999999':
        _prize_code = '0000000001'
    elif data_tmp != '9999999999':
        _prize_code = str(int(data_tmp) + 1)
        s_0 = ''
        for i in range(0, 10 - len(_prize_code)):
            s_0 += '0'
        _prize_code = s_0 + _prize_code
    _prize_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:8] + _prize_code
    return _prize_code


def get_award_name(test_data):
    award_name_list = []
    for i in range(0, len(test_data)):
        award_name = test_data[i][u'奖品名称']
        award_name_list.append(award_name)
    return award_name_list


def get_award_type(test_data):
    award_type_list = []
    for i in range(0, len(test_data)):
        award_type = test_data[i][u'奖励类型']
        award_type_list.append(award_type)
    return award_type_list


def get_award_level(test_data):
    award_level_list = []
    for i in range(0, len(test_data)):
        award_level = int(test_data[i][u'奖励等级'])
        award_level_list.append(award_level)
    return award_level_list


def get_wallet_amount(test_data):
    '''
    获取红包金额， 如果是实物，则取和其他不同的规则编号即可
    :return:
    '''
    wallet_amount_list = []
    for i in range(0, len(test_data)):
        wallet_amount = int(test_data[i][u'红包金额']) * 100
        wallet_amount_list.append(wallet_amount)
    return wallet_amount_list


def get_wallet_rule_code(test_data):
    '''
    根据红包金额。找对应的红包规则
    :return:
    '''
    wallet_amount_list = get_wallet_amount()
    wallet_rule_code_list = []
    for i in range(0, len(test_data)):
        wallet_rule_code_sql = "select rule_code from HD_WALLET_RULE T WHERE T.TOTAL_AMOUNT = %d" \
                               % wallet_amount_list[i]
        wallet_rule_code = dbutil_select(wallet_rule_code_sql)[0]
        wallet_rule_code_list.append(wallet_rule_code)
    return wallet_rule_code_list


def get_prize_count(test_data):
    prize_count_list = []
    for i in range(0, len(test_data)):
        prize_count = int(test_data[i][u'奖项份数'])
        prize_count_list.append(prize_count)
    return prize_count_list


def get_win_probability(test_data):
    win_probability_list = []
    for i in range(0, len(test_data)):
        win_probability = int(test_data[i][u'中奖概率（%）'])
        win_probability_list.append(win_probability)
    return win_probability_list


def create_lottery_award_tmp(test_data, prize_code,
                             lottery_code, create_time,
                             update_time, create_people,
                             update_people, version,
                             goods_name, platform_id):
    '''
    创建抽奖奖项
    :return:
    '''
    for i in range(0, len(test_data)):
        insert_lottery_award_sql = "insert into HD_LOTTERY_SETTING VALUES ('%s', '%s', '%s', '%s', %d, %d, '$%s', " \
                                   "'%s', '%s', '%s', %d, '%s', '%s', %d, '%s')" \
                                   % (prize_code, lottery_code, get_award_type()[i], get_wallet_rule_code()[i],
                                      get_prize_count()[i], get_prize_count()[i], create_time, update_time,
                                      create_people, update_people, version, get_award_level()[i], goods_name,
                                      get_win_probability()[i], platform_id)
        print insert_lottery_award_sql
        insert_db(insert_lottery_award_sql)
