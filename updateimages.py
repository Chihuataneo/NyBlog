import requests
from bs4 import BeautifulSoup
import time
from PIL import Image
import random

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_imgurls():
    page=1
    urls=[]
    while True:
        try:
            html=requests.get('http://www.socwall.com/wallpapers/page:{}/tagged:nature/'.format(page),headers=headers,timeout=30).text
        except:
            break
        table=BeautifulSoup(html,'lxml').find('ul',{'class':'wallpaperList'}).find_all('a',{'class':'image'})
        for a in table:
            urls.append('http://www.socwall.com/'+a.get('href'))
        if page==4:
            break
        page+=1
    imgurls=[]
    for url in urls:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            imgurl=BeautifulSoup(html,'lxml').find('a',{'class':'wallpaperImageLink wallpaperLink'}).get('href')
            if '1920x1080.jpg' in imgurl:
                imgurls.append('http://www.socwall.com/'+imgurl)
        except:
            continue
    return imgurls

def get_img(imgurl):
    content=requests.get(imgurl,headers=headers).content
    return content

def updateimages():
    try:
        imgurls=get_imgurls()
    except:
        date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        print(date,'Failed')
        return
    length=len(imgurls)
    img_paths=['collected_static/index/images/bg01.jpg','collected_static/index/images/bg02.jpg','collected_static/index/images/bg03.jpg','collected_static/images/wrapper.jpg']
    for path in img_paths:
        while True:
            index=random.randint(0,length)
            try:
                img=get_img(imgurls[index])
                with open(path,'wb') as imgfile:
                    imgfile.write(img)
                date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                print(date,path,'ok')
                break
            except:
                continue

while True:
    updateimages()
    time.sleep(3600*24)
