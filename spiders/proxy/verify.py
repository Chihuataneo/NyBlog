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

lock = threading.Lock()

f = open('./mysql_setting.json', 'r', encoding='utf8')
userdata = json.load(f)
f.close()


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
            if result in self.ip:
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
        date = time.strftime('%Y-%m-%d %X', time.localtime())
        cursor.execute("update tools_proxyip set time='%s' where ip='%s'" % (date, self.ip.split(':')[0]))
        print(date, 'update', self.ip)
        try:
            conn.commit()
        except:
            pass

    def delete(self):
        global cursor
        global conn
        date = time.strftime('%Y-%m-%d %X', time.localtime())
        print(date, 'delete', self.ip)
        cursor.execute("delete from tools_proxyip where ip='%s'" % (self.ip.split(':')[0]))
        try:
            conn.commit()
        except:
            pass


def verify():
    cursor.execute('select ip,port from tools_proxyip')
    iplist = []
    for row in cursor.fetchall():
        iplist.append("%s:%s" % (row[0], row[1]))
    threadings = []
    while len(iplist):
        count = 0
        while count < 20:
            try:
                ip = iplist.pop()
                count += 1
            except:
                break
            work = IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        threadings.clear()


if __name__ == '__main__':
    while True:
        conn = pymysql.connect(host=userdata['host'], user=userdata['user'], passwd=userdata['passwd'],
                               db=userdata['db'], port=userdata['port'], charset='utf8')
        cursor = conn.cursor()
        verify()
        time.sleep(180)
        cursor.close()
        conn.commit()
        conn.close()
