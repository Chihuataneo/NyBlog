from tools.models import ProxyIp


def select_ip(page, num):
    rows = ProxyIp.objects.order_by('-time').all()[(page - 1) * num:page * num]
    result = []
    for row in rows:
        result.append(row.to_dict())
    return result
