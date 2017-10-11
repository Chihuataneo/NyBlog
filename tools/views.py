from django.http import HttpResponse
from django.shortcuts import render

from ratelimit.decorators import ratelimit

from tools.logic import logic_proxyip
from tools.logic.logic_coder import *

def limit_rate(group,request):
    if request.user.is_authenticated():
        return None
    else:
        return '100/10m'

@ratelimit(key='ip', rate=limit_rate)
def proxy(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return HttpResponse(json.dumps({'status':False}), content_type="application/json")

    try:
        page = request.GET['page']
        num = request.GET['num']
        token = request.GET['token']
        timestamp = request.GET['t']
    except:
        return render(request, "proxy.html")
    result = logic_proxyip.get_proxy_ip(page, num, token, timestamp)
    return HttpResponse(json.dumps(result), content_type="application/json")


def downloader(request):
    return render(request, "downloader.html")


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
