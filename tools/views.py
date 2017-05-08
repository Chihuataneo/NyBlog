import json

from django.http import HttpResponse
from django.shortcuts import render

import tools.logic.logic_proxyip as proxyip
from tools.logic.logic_coder import *


def proxy(request):
    try:
        page = int(request.GET['page'])
        num = int(request.GET['num'])
    except:
        return render(request, "proxy.html")
    result = proxyip.select_ip(page, num)
    return_data = {"status": "true", "list": result}
    return HttpResponse(json.dumps(return_data), content_type="application/json")


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
