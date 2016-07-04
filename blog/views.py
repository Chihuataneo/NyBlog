from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login as auth_login,logout
import base64
from  blog.article import *
from blog.books import *


def islogin(request):
    buttontext="登录"
    url="../login"
    classvalue="button special"
    num=2
    if request.user.is_authenticated():
        buttontext=request.user.get_username()
        url="../userinfor"
        classvalue=""
        num=1
    return [buttontext,url,classvalue,num]

def index(request):
    home_html=render_to_string('index.html')
    return HttpResponse(home_html)

def home(request):
    loginvalue=islogin(request)
    result=get_articles(page=1,num=2)
    articles=[]
    for item in result:
        article={}
        article['id']=item.id
        article['title']=item.title
        article['category']=item.category
        article['introduction']=item.introduction
        article['date']=item.pub_date
        articles.append(article)
    categorys=get_category()
    result=get_books(1,6)
    books=[]
    for item in result:
        book={}
        book['id']=item.id
        book['title']=item.title[:13]+'..'
        book['introduction']=item.introduction[:80]+"..."
        book['imgurl']=item.imgurl
        books.append(book)
    return render(request, 'home.html', {'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3],'articles':articles,'categorys':categorys,'books':books})

def login_GET(request):
    buttontext="登录"
    url="../login"
    classvalue="button special"
    num=2
    if request.user.is_authenticated():
        buttontext=request.user.get_username()
        url="../userinfor"
        classvalue=""
        num=1
    login_html=render_to_string('login.html')
    return render(request, 'login.html', {'name': buttontext,'url':url,'class':classvalue,'num':num})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        passwd=request.POST['password']
        passwd=base64.b64decode(passwd)
        user=authenticate(username=username,password=passwd)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return home(request)
            else:
                return login_GET(request)
        else:
            return login_GET(request)
    else:
        return login_GET(request)

def blog_logout(request):
    logout(request)
    return home(request)

def books(request):
    loginvalue=islogin(request)
    try:
        page=int(request.GET['page'])
        num=int(request.GET['num'])
    except:
        page=1
        num=6
    if page<=1:
        prepage=1
    else:
        prepage=page-1
    nextpage=page+1
    result=get_books(page,num)
    books=[]
    for item in result:
        book={}
        book['id']=item.id
        book['title']=item.title
        book['introduction']=item.introduction[:80]+"..."
        book['imgurl']=item.imgurl
        book['category']=item.category
        book['date']=item.pub_date
        books.append(book)
    categorys=get_category()
    return render(request, 'books.html', {'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3],'categorys':categorys,'books':books,'prepage':prepage,'nextpage':nextpage})

def articles(request):
    loginvalue=islogin(request)
    try:
        page=int(request.GET['page'])
        num=int(request.GET['num'])
    except:
        page=1
        num=6
    if page<=1:
        prepage=1
    else:
        prepage=page-1
    nextpage=page+1
    result=get_articles(page,num)
    articles=[]
    for item in result:
        article={}
        article['id']=item.id
        article['title']=item.title
        article['category']=item.category
        article['introduction']=item.introduction
        article['date']=item.pub_date
        articles.append(article)
    categorys=get_category()
    return render(request, 'articles.html', {'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3],'categorys':categorys,'articles':articles,'prepage':prepage,'nextpage':nextpage})


def userinfor(request):
    return home(request)

def book(request):
    try:
        bookid=request.GET['bookid']
        bookid=int(bookid)
    except:
        return books(request)
    loginvalue=islogin(request)
    item=get_book(bookid)
    book={}
    book['id']=item.id
    book['title']=item.title
    book['introduction']=item.introduction[:80]+"..."
    book['imgurl']=item.imgurl
    book['category']=item.category
    book['date']=item.pub_date
    book['downloadurl']=item.downloadurl
    return render(request, 'book.html',{'book':book,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def article(request):
    try:
        articleid=request.GET['articleid']
    except:
        return articles(request)
    loginvalue=islogin(request)
    item=get_article(articleid)
    article={}
    article['id']=item.id
    article['title']=item.title
    article['category']=item.category
    article['date']=item.pub_date
    return render(request, 'article.html',{'article':article,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def article_content(request):
    id=request.GET['id']
    item=get_article(id)
    return HttpResponse(item.content)

def categorys(request):
    return home(request)
