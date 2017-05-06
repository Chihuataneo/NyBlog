from django.shortcuts import render
import tools.proxyip as proxyip
from django.http import HttpResponse
import json

def proxy(request):
    try:
        page=int(request.GET['page'])
        num=int(request.GET['num'])
    except:
        return render(request,"proxy.html")
    result=proxyip.select_ip(page,num)
    return_data={"status":"true","list":result}
    return HttpResponse(json.dumps(return_data),content_type="application/json")
