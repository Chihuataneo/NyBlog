from tools.models import ProxyIp
import hashlib


def select_ip(page, num):
    rows = ProxyIp.objects.order_by('-time').all()[(page - 1) * num:page * num]
    result = []
    for row in rows:
        result.append(row.to_dict())
    return result


def get_proxy_ip(page, num, token, timestamp):
    md5 = hashlib.md5()
    md5.update((page + num + timestamp).encode(encoding="utf-8"))
    md5_token = md5.hexdigest()
    if (md5_token == token):
        try:
            items = select_ip(int(page), int(num))
        except:
            items = []
    else:
        items = []
    result = {"status": "true", "list": items}
    return result
