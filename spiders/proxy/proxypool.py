import requests
import threading
import time
import pymysql
import json

from proxy_spiders.spider_ipcn import SpiderIpcn
from proxy_spiders.spider_66ip import SpiderIP66
from proxy_spiders.spider_kxdaili import SpiderKxdaili
from proxy_spiders.spider_89ip import SpiderIP89
from proxy_spiders.spider_data5u import SpiderData5u
from proxy_spiders.spider_ip181 import SpiderIP181
from proxy_spiders.spider_xicidaili import SpiderXicidaili

class IsEnable(threading.Thread):
    def __init__(self, ip):
        super(IsEnable, self).__init__()
        self.ip = ip
        self.proxies = {
            'http': 'http://%s' % ip
        }

    def run(self):
        try:
            html = requests.get('http://httpbin.org/ip', proxies=self.proxies, timeout=5).text
            result = eval(html)['origin']
            if len(result.split(',')) == 2:
                return
            if result in self.ip:
                with lock:
                    self.insert_into_sql()
        except:
            return

    def insert_into_sql(self):
        global cursor
        global conn
        global crawl_ip_count
        try:
            date = time.strftime('%Y-%m-%d %X', time.localtime())
            cursor.execute("insert into tools_proxyip(ip,port,time) values" + str(
                (self.ip.split(':')[0], self.ip.split(':')[1], date)))
            conn.commit()
            crawl_ip_count += 1
        except:
            pass


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


if __name__ == '__main__':
    lock = threading.Lock()
    f = open('./mysql_setting.json', 'r', encoding='utf8')
    user_data = json.load(f)
    f.close()

    crawlers = [SpiderIP66, SpiderXicidaili, SpiderIpcn, SpiderIP89, SpiderData5u]
    while True:
        crawl_ip_count = 0
        conn = pymysql.connect(host=user_data['host'], user=user_data['user'], passwd=user_data['passwd'],
                               db=user_data['db'], port=user_data['port'], charset='utf8')
        cursor = conn.cursor()
        result = []
        tasks = []
        for crawler in crawlers:
            task = crawler()
            task.setDaemon(True)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            try:
                result += task.result
            except:
                continue
        while (len(result)):
            num = 0
            while (num < 50):
                try:
                    ip = result.pop()
                except:
                    break
                work = IsEnable(ip)
                work.setDaemon(True)
                work.start()
                num += 1
            time.sleep(5)
        try:
            conn.commit()
        except:
            pass
        cursor.close()
        conn.close()
        print('[%s][ProxyPool]Crawl IP Count:' % get_current_time(), crawl_ip_count)
        print('[%s][ProxyPool][Sleeping]' % get_current_time())
        time.sleep(300)
