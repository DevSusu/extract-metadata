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

    with open("data/data.js",'w') as f:
        f.write(print_str+"\";")

    ex.save(filename="images_metadata_{}.csv".format(datetime.datetime.now().strftime('%y%m%d')))
