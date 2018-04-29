import requests
from bs4 import BeautifulSoup
import logging
import time
import threading


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def crawl():
    result = []
    for page in range(1, 10):
        url = 'https://www.kuaidaili.com/ops/proxylist/{}/'.format(page)
        try:
            html = requests.get(url, headers=headers, timeout=30).text
            table = BeautifulSoup(html, 'lxml').find(
                'div', {'id': 'freelist'}).find('table').find_all('tr')
        except Exception as e:
            print('[%s][Spider][kuaidaili]ERROR!' % get_current_time(), e)
            continue
        for tr in table[1:]:
            try:
                ip = tr.find('td', {'data-title': 'IP'}).get_text()
                port = tr.find('td', {'data-title': 'PORT'}).get_text()
                ip = ip + ':' + port
                result.append(ip)
            except:
                pass
    print('[%s][Spider][kuaidaili]OK!' %
          get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderKuaidaili(threading.Thread):
    def __init__(self):
        super(SpiderKuaidaili, self).__init__()

    def run(self):
        self.result = crawl()
