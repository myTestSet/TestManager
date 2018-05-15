# -*- coding:utf-8 -*-

# __author__ = 'liuzunrui'
import xlrd


class ExcelUtil:
    def __init__(self, filepath, sheetname):
        self.data = xlrd.open_workbook(filepath)
        self.table = self.data.sheet_by_name(sheetname)
        self.keys = self.table.row_values(0)
        self.rownums = self.table.nrows
        self.colnums = self.table.ncols

    def get_data(self):
        if self.rownums <= 1:
            print '行数不正确'
        else:
            r = []
            j = 1
            for i in range(self.rownums-1):
                s = {}
                values = self.table.row_values(j)
                for x in range(self.colnums):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r
