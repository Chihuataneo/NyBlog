from tools.models import ProxyIp
import hashlib
import time
import base64
import json
import random


def select_ip(page, num):
    rows = ProxyIp.objects.order_by('-time').all()[(page - 1) * num:page * num]
    result = []
    for row in rows:
        result.append(row.to_dict())
    return result


def get_proxy_ip(page, num, token, timestamp):
    md5 = hashlib.md5()
    md5.update((page + num + str(timestamp)).encode(encoding="utf-8"))
    md5_token = md5.hexdigest()
    if (abs(time.time() - float(timestamp)) > 60):
        items = []
    elif (md5_token == token):
        try:
            items = select_ip(int(page), int(num))
        except:
            items = []
    else:
        items = []
    encode_result = encode_str(json.dumps(items))
    result = {"status": "true", "list": encode_result}
    return result


def generate_junk_data():
    ip_list = []
    for i in range(15):
        ip = '%s.%s.%s.%s' % (
            random.randint(100, 200), random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        port = random.randint(1000, 30000)
        format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(20, 100)))
        ip_list.append({
            'ip': ip,
            'port': port,
            'time': format_time
        })
    encode_result = encode_str(json.dumps(ip_list))
    result = {"status": "true", "list": encode_result}
    return result


def from_char_code(a, *b):
    return chr(a % 65536) + ''.join([chr(i % 65536) for i in b])


def encode_str(string):
    secret_key = 'nyloner'
    key_length = len(secret_key)
    string = base64.b64encode(string.encode('utf-8')).decode('utf-8')
    code = ''
    for i in range(len(string)):
        index = i % key_length
        code += from_char_code(ord(string[i]) ^ ord(secret_key[index]))
    result = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    return result


def get_client_ip_info(request):
    remote_ip = ''
    forwarded_ip = ''
    if 'REMOTE_ADDR' in request.META:
        remote_ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        forwarded_ip = request.META['HTTP_X_FORWARDED_FOR']
    return {
        'remote_ip': remote_ip,
        'forwarded_ip': forwarded_ip
    }


def create_session_limit(request):
    timestamp = time.time()
    request.session['session_limit'] = timestamp


def check_sesssion_limit(request):
    try:
        session_limit = request.session['session_limit']
    except:
        return False
    timestamp = time.time()
    if timestamp > session_limit + 120:
        return False
    return True
