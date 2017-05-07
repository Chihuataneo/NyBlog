import json

from django.http import HttpResponse
from django.shortcuts import render

import tools.logic.logic_proxyip as proxyip


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
    return render(request, "proxy.html")
