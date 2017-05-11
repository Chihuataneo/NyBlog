import requests
import threading
import time
import json
import pymysql

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


class IsEnable(threading.Thread):
    def __init__(self, ip):
        super(IsEnable, self).__init__()
        self.ip = ip
        self.proxies = {
            'http': 'http://%s' % (ip)
        }

    def run(self):
        try:
            html = requests.get('http://httpbin.org/ip', proxies=self.proxies, timeout=3).text
            result = eval(html)['origin']
            if len(result.split(',')) == 2:
                with lock:
                    self.delete()
                return
            elif result in self.ip:
                with lock:
                    self.update()
            else:
                with lock:
                    self.delete()
        except:
            with lock:
                self.delete()

    def update(self):
        global cursor
        global conn
        try:
            date = get_current_time()
            cursor.execute("update tools_proxyip set time='%s' where ip='%s'" % (date, self.ip.split(':')[0]))
            conn.commit()
            print('[%s][ProxyPool][Update]' % date, self.ip)
        except:
            pass

    def delete(self):
        global cursor
        global conn
        try:
            cursor.execute("delete from tools_proxyip where ip='%s'" % (self.ip.split(':')[0]))
            conn.commit()
            print('[%s][ProxyPool][Delete]' % get_current_time(), self.ip)
        except:
            pass


def verify():
    cursor.execute('select ip,port from tools_proxyip')
    ip_list = []
    for row in cursor.fetchall():
        ip_list.append("%s:%s" % (row[0], row[1]))
    while len(ip_list):
        count = 0
        while count < 20:
            try:
                ip = ip_list.pop()
                count += 1
            except:
                break
            work = IsEnable(ip)
            work.setDaemon(True)
            work.start()
        time.sleep(5)


if __name__ == '__main__':
    lock = threading.Lock()
    f = open('./mysql_setting.json', 'r', encoding='utf8')
    user_data = json.load(f)
    f.close()
    while True:
        conn = pymysql.connect(host=user_data['host'], user=user_data['user'], passwd=user_data['passwd'],
                               db=user_data['db'], port=user_data['port'], charset='utf8')
        cursor = conn.cursor()
        verify()
        time.sleep(180)
        cursor.close()
        conn.commit()
        conn.close()
