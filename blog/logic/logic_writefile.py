import time
import os
from blog.models import File


def handle_uploaded_file(f, title):
    filename = f.name
    files = os.listdir('collected_static/files')
    if filename in files:
        filename = time.strftime("%Y%m%d_%H%M", time.localtime()) + '_' + filename
    uploadfile = File()
    uploadfile.title = title
    uploadfile.downloadurl = '../static/files/%s' % (filename)
    uploadfile.filename = filename
    uploadfile.save()
    with open('collected_static/files/%s' % filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
