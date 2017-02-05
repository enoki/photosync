from exifpy import exifread
import sys
import os
import scandir

def getYearMonthDay(path):
    with open(path, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        dateTimeParts = str(dateTaken).split(' ')
        parts = dateTimeParts[0].split(':')
    return parts[0], parts[1], parts[2]

rootPath = 'e:/Pictures'
path = sys.argv[1]
year,month,day = getYearMonthDay(path)
filename = os.path.basename(path)
dstPath = '%s/%s/%s/%s/%s' % (rootPath, year, month, day, filename)
print dstPath

print 'mkdir %s' % os.path.dirname(dstPath)
print 'mklink %s %s' % (dstPath, path)
