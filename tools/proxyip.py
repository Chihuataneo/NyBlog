from tools.models import ProxyIp

def select_ip(page,num):
    fromnum=(page-1)*num
    tonum=page*num
    rows=ProxyIp.objects.order_by('-time').all()[fromnum:tonum]
    result=[]
    for row in rows:
        result.append(row.to_dict())
    return result
