#!C:\Users\OCM\workspace\python\image_metadata/Scripts python
# -*- coding: utf-8 -*-

from os import listdir, makedirs
from os.path import isfile, join, exists

import datetime
import metadata as meta
from excel import Excel

def filenames(dirpath):
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

if not exists('images'):
    makedirs('images')
    print("images 폴더를 만들었습니다. images 폴더에 분석하고자 하는 사진을 넣어주세요")

files = filenames('images/')
print("{}개 파일".format(len(files)))

ex = Excel({ 'column_names' : ['filename'] + meta.DEFAULT_TAGS })

print_str = "var image_data=\""

for fname in files:
    meta_infos = meta.extract_exif(f=open('images/'+fname,'rb'))
    meta_infos['filename'] = fname
    tmp_row = ex.add_row(meta_infos)

    print_str += "{},{},{},{}\\n".format(
        tmp_row[0],
        tmp_row[1],
        tmp_row[2],
        tmp_row[3]
    )

if not exists('data'):
    makedirs('data')

with open("data/data.js",'w') as f:
    f.write(print_str+"\";")

ex.save(filename="data/images_metadata_{}.xlsx".format(datetime.datetime.now().strftime('%y%m%d')))
