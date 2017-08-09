# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import datetime

import exifread
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


DEFAULT_TAGS = [
    'Image DateTime',
    'GPS GPSLatitude',
    'GPS GPSLongitude',

    'Image Make',
    'Image Model',

    'GPS GPSAltitude',

    'EXIF DateTimeOriginal',
    'EXIF LensModel'
]

def to_degrees(values):
    # Ratio class https://github.com/ianare/exif-py/blob/develop/exifread/utils.py
    return float(values[0].num)/float(values[0].den) + float(values[1].num)/float(values[1].den)/60 + float(values[2].num)/float(values[2].den)/3600

def extract_exif(f, keys=DEFAULT_TAGS):
    tags = exifread.process_file(f)
    result = {}
    for key in keys:
        if key not in tags:
            continue

        if type(tags[key].values) is list and len(tags[key].values) == 3:
            result[key] = to_degrees(tags[key].values)
        else:
            result[key] = tags[key].__str__()

    # return { key : tags[key].__str__() for key in keys if key in tags }
    return result

def filenames(dirpath):
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

files = filenames('images/')
print("{}개 파일".format(len(files)))

ex = Excel({ 'column_names' : ['filename'] + DEFAULT_TAGS })

print_str = "var image_data=\""

for fname in files:
    meta_infos = extract_exif(f=open('images/'+fname,'rb'))
    meta_infos['filename'] = fname
    tmp_row = ex.add_row(meta_infos)

    print_str += "{},{},{},{}\\n".format(
        tmp_row[0],
        tmp_row[1],
        tmp_row[2],
        tmp_row[3]
    )

with open("data/data.js",'w') as f:
    f.write(print_str+"\";")

ex.save(filename="images_metadata_{}.xlsx".format(datetime.datetime.now().strftime('%y%m%d')))
