import requests
import json
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Host": "ip.chinaz.com",
    "Referer": "http://ip.chinaz.com/ipbatch",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_ip_info(ip):
    url = 'http://ip.chinaz.com/ajaxsync.aspx?at=ipbatch'
    result = {}
    try:
        html = requests.post(url, headers=headers, data={'ip': ip}, timeout=5).text
        location = re.findall("location:'(.*?)'", html)[0]
        result['location'] = location
    except:
        return {'status': 'false'}
    result['status'] = 'true'
    return result
