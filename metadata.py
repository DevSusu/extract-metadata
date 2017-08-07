import exifread

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

if __name__ == "__main__":
    f = open('images/P20160201_190418442_7E333CAF-B277-4162-ACF9-7DD0041B4F5F.JPG', 'rb')
    tags = exifread.process_file(f)

    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote'):
            print("Key: %s, value %s" % (tag, tags[tag]) )
