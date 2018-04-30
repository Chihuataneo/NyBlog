from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import time

from ratelimit.decorators import ratelimit

from tools.logic import logic_proxyip
from tools.logic.logic_coder import *
from tools.logic.logic_converter import *
from tools.logger.tool_logger import tool_logger


def limit_rate(group, request):
    if request.user.is_authenticated():
        return None
    else:
        return '100/10m'


@ratelimit(key='ip', rate=limit_rate)
def proxy(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        ip_info = logic_proxyip.get_client_ip_info(request)
        tool_logger.warning('Type:ratelimit\tMessage:' + json.dumps(ip_info))
        return HttpResponse(json.dumps({'status': False}), content_type="application/json")

    try:
        page = request.GET['page']
        num = request.GET['num']
        token = request.GET['token']
        timestamp = int(request.GET['t'])
    except:
        logic_proxyip.create_session_limit(request)
        return render(request, "proxy.html")
    if not logic_proxyip.check_sesssion_limit(request):
        return HttpResponse(json.dumps({'status': False, 'msg': 'emmm...'}),
                            content_type="application/json")
    result = logic_proxyip.get_proxy_ip(page, num, token, timestamp)
    return HttpResponse(json.dumps(result), content_type="application/json")


def tools(request):
    return coder(request)


def coder(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return render(request, "coder.html", {'client_ip': ip})


def tool_ip_query(request):
    try:
        ip = request.GET['ip']
    except:
        return_data = {"status": "false"}
        return HttpResponse(json.dumps(return_data), content_type="application/json")
    ip_info = get_ip_info(ip)
    return HttpResponse(json.dumps(ip_info), content_type="application/json")


def converter(request):
    return render(request, 'converter.html')


def upload_doc(request):
    if request.method == 'GET':
        return HttpResponseRedirect('converter')
    try:
        file_data = request.FILES.get('file_data')
        file_name = file_data.name
        if is_file_in_dest_dir(file_name):
            file_name = str(int(time.time() * 1000)) + '_' + file_name
        with open('%s/%s' % (CONVERTER_CONF['dest_dir'], file_name), 'wb') as f:
            for chunk in file_data.chunks():
                f.write(chunk)
            f.close()
        request.session['file_name'] = file_name

        file_type = file_name.split('.')[-1]
        supported_types = []
        if file_type in CONVERTER_CONF['supported_types']:
            supported_types = CONVERTER_CONF['supported_types'][file_type]
        return HttpResponse(json.dumps({'status': 'OK', 'supported_types': supported_types}),
                            content_type="application/json")
    except:
        return HttpResponse(json.dumps({'status': 'False'}), content_type="application/json")


def download_doc(request):
    if request.method == 'GET':
        try:
            download_type = request.GET['type']
        except:
            return HttpResponseRedirect('converter')
        if download_type not in CONVERTER_CONF['allowed_type']:
            return HttpResponseRedirect('converter')
        response = DOWNLOAD_FUNC[download_type](request)
        if response == None:
            return HttpResponseRedirect('converter')
        return response
    else:
        return HttpResponseRedirect('converter')


def check_ip(request):
    remote_ip = ''
    forwarded_ip = ''
    if 'REMOTE_ADDR' in request.META:
        remote_ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        forwarded_ip = request.META['HTTP_X_FORWARDED_FOR']
    info = {
        'remote_ip': remote_ip,
        'forwarded_ip': forwarded_ip
    }
    return HttpResponse(json.dumps(info), content_type="application/json")
