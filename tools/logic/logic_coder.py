import requests
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "ip.taobao.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_ip_info(ip):
    url = 'http://ip.taobao.com/service/getIpInfo2.php?ip=' + ip
    try:
        result = requests.get(url, headers=headers, timeout=5).text
        result = json.loads(result)
    except:
        return {'status': 'false'}
    result['status'] = 'true'
    return result
