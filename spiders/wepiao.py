import requests
import json
import datetime
import re
import pymysql
import time


ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
f=open('./mysql_setting.json','r',encoding='utf8')
userdata=json.load(f)
f.close()
conn=pymysql.connect(host=userdata['host'],user=userdata['user'],passwd=userdata['passwd'],db=userdata['db'],port=userdata['port'],charset='utf8')
cursor=conn.cursor()

headers = {
    'Host':'piaofang.wepiao.com',
    'Referer':'https://piaofang.wepiao.com/?dateStart=2017-01-08&dateEnd=2017-01-08&scheduleState=day',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type':'application/json'}

boxoffice_keys=['movieId','movieName','movieNameEnglish','releaseDate','showDate','productBoxOffice','productTotalBoxOffice','productBoxOfficeRate','productScheduleRate','productTicketSeatRate']
exists={}

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d - oneday
    return day

def product_box_office(day):
    data={
    "movieFilter":{"showDateFrom":day,"showDateTo":day,"sortType":"desc"},
    "paging":{"pageSize":"30"},
    "lang":"cn"
    }
    html=requests.post('https://piaofang.wepiao.com/api/v1/index',data=json.dumps(data),headers=headers,timeout=30).text
    json_data=json.loads(html)
    json_data=json_data['movieBoxOffices']
    movies=[]
    for item in json_data:
        movie={}
        for key in boxoffice_keys:
            try:
                movie[key]=item[key]
            except:
                movie[key]=''
        movies.append(movie)
    return movies

def movie_infor(movie_id):
    data={
    'id':movie_id,
    "lang":"cn"
    }
    html=requests.post('https://piaofang.wepiao.com/api/v1/movie/detail',data=json.dumps(data),headers=headers,timeout=30).text
    json_data=json.loads(html)
    json_data=json_data['data']['movie']
    return json_data

def exist_movies():
    global exists
    global cursor
    cursor.execute("select movieId from tools_movie")
    rows=cursor.fetchall()
    for row in rows:
        exists[row[0]]=1

def insert_into_movie(movie):
    global cursor
    line=[]
    for key in ['id','name','type','time','score','poster','date','director','actor','plot']:
        try:
            if key=='score':
                value=float(movie[key])
                line.append(float(movie[key]))
            else:
                line.append(movie[key])
        except:
            line.append('')
    cursor.execute("insert into tools_movie(movieId,movieName,movie_type,time_length,score,pictureUrl,date,director,actors,plot) values"+str(tuple(line)))

def insert_into_boxoffice(movies):
    global cursor
    not_exists=[]
    for movie in movies:
        line=[]
        movieid=movie['movieId']
        if str(movieid) not in exists:
            not_exists.append(str(movieid))
        for key in ['movieId','movieName','movieNameEnglish','releaseDate','showDate']:
            try:
                line.append(str(movie[key]).replace('\r','').replace('\n',''))
            except:
                line.append('')
        for key in ['productBoxOffice','productTotalBoxOffice','productBoxOfficeRate','productScheduleRate','productTicketSeatRate']:
            try:
                line.append(float(movie[key]))
            except:
                line.append('')
        cursor.execute("insert into tools_boxoffice(movieId,movieName,movieNameEnglish,releaseDate,showDate,productBoxOffice,productTotalBoxOffice,productBoxOfficeRate,productScheduleRate,productTicketSeatRate) values"+str(tuple(line)))
    while len(not_exists):
        try:
            movie_id=not_exists.pop()
            detail=movie_infor(movie_id)
        except:
            continue
        try:
            insert_into_movie(detail)
        except:
            continue
        exists[movie_id]=1
    conn.commit()

def update():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    day=datetime.datetime.now()
    text=open('days.txt','r').read()
    f=open('days.txt','w')
    for i in range(10):
        day=day_get(day)
        day_str=str(day).split(' ')[0]
        if day_str in text:
            f.write(day_str+'\n')
            continue
        try:
            movies=product_box_office(day_str)
            insert_into_boxoffice(movies)
            print(timenow,day_str,'ok')
            f.write(day_str+'\n')
        except:
            print(timenow,day_str,'failed')
    f.close()

if __name__=='__main__':
    exist_movies()
    while True:
        update()
        time.sleep(3600*24)
