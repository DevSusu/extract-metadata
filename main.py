from os import listdir
from os.path import isfile, join

import datetime
import metadata as meta
from excel import Excel

def filenames(dirpath):
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

if __name__ == "__main__":
    files = filenames('images/')
    print("{}개 파일".format(len(files)))

    ex = Excel({ 'column_names' : ['filename'] + meta.DEFAULT_TAGS })

    for fname in files:
        print(fname)
        meta_infos = meta.extract_exif(f=open('images/'+fname,'rb'))
        meta_infos['filename'] = fname
        ex.add_row(meta_infos)

    ex.save(filename="images_metadata_{}.xlsx".format(datetime.datetime.now().strftime('%y%m%d')))
