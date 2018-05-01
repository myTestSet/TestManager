# -*- coding:utf-8 -*-

# __author__ = 'liuzunrui'

from utils.fileUtil.readfile import ExcelUtil


def get_test_data(filename, sheetname):
    data = ExcelUtil("filedata/" + filename + ".xls", (u'%s' % sheetname))
    print "../filedata/" + filename + ".xls", (u'%s' % sheetname)
    test_data = data.get_data()
    return test_data
