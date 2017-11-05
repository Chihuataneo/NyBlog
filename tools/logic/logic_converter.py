import os
from urllib import parse
from django.http import StreamingHttpResponse

CONVERTER_CONF = {
    'dest_dir': 'converted_files',
    'allowed_type': ['pdf', 'html', 'png', 'txt'],
    'supported_types': {
        'xls': ['pdf', 'html', 'png', 'txt'],
        'xlsx': ['pdf', 'html', 'png', 'txt'],
        'doc': ['pdf', 'html', 'png', 'txt'],
        'docx': ['pdf', 'html', 'png', 'txt'],
        'pdf': ['png', 'txt']
    }
}


def is_file_in_dest_dir(filename):
    file_path = CONVERTER_CONF['dest_dir'] + '/' + filename
    return os.path.isfile(file_path)


def convert_to_html(src_file):
    command = "libreoffice --headless --convert-to html --outdir %s %s" % (CONVERTER_CONF['dest_dir'], src_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.html')
    return os.path.isfile(file_path)


def convert_to_txt(src_file):
    command = "libreoffice --headless --convert-to txt --outdir %s %s" % (CONVERTER_CONF['dest_dir'], src_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.txt')
    return os.path.isfile(file_path)


def doc_to_pdf(src_file):
    command = "libreoffice --headless --convert-to pdf --outdir %s %s" % (CONVERTER_CONF['dest_dir'], src_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.pdf')
    return os.path.isfile(file_path)


def doc_to_image(src_file):
    command = "libreoffice --headless --convert-to png --outdir %s %s" % (CONVERTER_CONF['dest_dir'], src_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.png')
    return os.path.isfile(file_path)


def html_to_image(src_file):
    dest_file = src_file.replace('.html', '.png')
    command = "wkhtmltoimage %s %s" % (src_file, dest_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.png')
    return os.path.isfile(file_path)


def pdf_to_image(src_file):
    command = "libreoffice --headless --convert-to png --outdir %s %s" % (CONVERTER_CONF['dest_dir'], src_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.png')
    return os.path.isfile(file_path)


def html_to_pdf(src_file):
    dest_file = src_file.replace('.html', '.pdf')
    command = "wkhtmltopdf %s %s" % (src_file, dest_file)
    os.system(command)
    file_path = src_file.replace('.' + src_file.split('.')[-1], '.pdf')
    return os.path.isfile(file_path)


def excel_to_pdf(src_file):
    status = convert_to_html(src_file)
    if not status:
        return False
    html_file_path = src_file.replace('.' + src_file.split('.')[-1], '.html')
    status = html_to_pdf(html_file_path)
    remove_file(html_file_path)
    return status


def excel_to_image(src_file):
    status = convert_to_html(src_file)
    if not status:
        return False
    html_file_path = src_file.replace('.' + src_file.split('.')[-1], '.html')
    status = html_to_image(html_file_path)
    remove_file(html_file_path)
    return status


def remove_file(file_path):
    command = 'rm %s' % (file_path)
    os.system(command)


def send_file(file_path):
    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        remove_file(file_path)

    response = StreamingHttpResponse(file_iterator(file_path))
    file_name = file_path.split('/')[-1]
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(parse.quote(file_name, 'utf-8'))
    return response


def download_pdf(request):
    try:
        file_name = request.session['file_name']
    except:
        return None
    file_type = file_name.split('.')[-1]
    src_file = '%s/%s' % (CONVERTER_CONF['dest_dir'], file_name)
    if file_type == 'doc' or file_type == 'docx':
        status = doc_to_pdf(src_file)
        if not status:
            return None
    elif file_type == 'xls' or file_type == 'xlsx':
        status = excel_to_pdf(src_file)
        if not status:
            return None
    else:
        return None
    return send_file(src_file.replace('.' + file_type, '.pdf'))


def download_png(request):
    try:
        file_name = request.session['file_name']
    except:
        return None
    file_type = file_name.split('.')[-1]
    src_file = '%s/%s' % (CONVERTER_CONF['dest_dir'], file_name)
    if file_type == 'doc' or file_type == 'docx':
        status = doc_to_image(src_file)
        if not status:
            return None
    elif file_type == 'xls' or file_type == 'xlsx':
        status = excel_to_image(src_file)
        if not status:
            return None
    elif file_type == 'pdf':
        status = pdf_to_image(src_file)
        if not status:
            return None
    else:
        return None
    return send_file(src_file.replace('.' + file_type, '.png'))


def download_html(request):
    try:
        file_name = request.session['file_name']
    except:
        return None
    file_type = file_name.split('.')[-1]
    src_file = '%s/%s' % (CONVERTER_CONF['dest_dir'], file_name)
    status = convert_to_html(src_file)
    if not status:
        return None
    return send_file(src_file.replace('.' + file_type, '.html'))


def download_txt(request):
    try:
        file_name = request.session['file_name']
    except:
        return None
    file_type = file_name.split('.')[-1]
    src_file = '%s/%s' % (CONVERTER_CONF['dest_dir'], file_name)
    status = convert_to_html(src_file)
    if not status:
        return None
    status = convert_to_txt(src_file.replace('.' + file_type, '.html'))
    if not status:
        return None
    remove_file(src_file.replace('.' + file_type, '.html'))
    return send_file(src_file.replace('.' + file_type, '.txt'))


DOWNLOAD_FUNC = {
    'pdf': download_pdf,
    'png': download_png,
    'html': download_html,
    'txt': download_txt
}
