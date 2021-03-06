#!C:\Users\OCM\workspace\python\image_metadata/Scripts python
# -*- coding: utf-8 -*-

from openpyxl import Workbook

class Excel(object):
    def __init__(self, arg):
        super(Excel, self).__init__()

        self.wb = Workbook()
        self.ws = self.wb.active

        if 'column_names' in arg:
            self.set_column_names(arg['column_names'])

    def set_column_names(self, column_names):
        self.column_names = column_names
        for col,name in enumerate(column_names):
            self.ws.cell(column=col+1, row=1, value=name)

    def add_row(self, obj):
        if type(obj) is dict:
            row = []
            for col in self.column_names:
                if col in obj:
                    row.append(obj[col])
                else:
                    row.append("")

            self.ws.append(row)
            return row

        else:
            return None

    def save(self, filename='metadata.xlsx', encoding='utf-8'):
        self.wb.save(filename)
