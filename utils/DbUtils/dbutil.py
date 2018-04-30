# -*- coding:utf-8 -*-
# @Author= 'liuzunrui'
# @Time :2018/4/30 下午3:12

import cx_Oracle
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def dbutil_select(sql):
    user = 'zfpt_kf'
    password = 'zfpt_kf'

    host = "192.168.80.131"
    port = 15210
    dbname = "htjcdb8"

    dsn = cx_Oracle.makedsn(host, port, dbname)

    db = cx_Oracle.connect(user, password, dsn)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def insert_db(sql):
    '''
    增加数据
    :param sql:
    :return:
    '''
    user = 'zfpt_kf'
    password = 'zfpt_kf'
    host = "192.168.80.131"
    port = 15210
    dbname = "htjcdb8"
    dsn = cx_Oracle.makedsn(host, port, dbname)
    db = cx_Oracle.connect(user, password, dsn)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()