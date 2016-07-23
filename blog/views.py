from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login as auth_login,logout
import base64
from blog.article import *
from blog.books import *
from blog.forms import UploadFileForm,ShareFileForm
from blog.writefile import handle_uploaded_file
from blog.files import get_files
from blog.models import Book

def islogin(request):
    buttontext="登录"
    url="../login"
    classvalue="button special"
    num=2
    if request.user.is_authenticated():
        buttontext=request.user.get_username()
        url="../user"
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
        article['categorys']=item.category.split(',')
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
        url="../user"
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
        book['categorys']=item.category.split(',')
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
        article['categorys']=item.category.split(',')
        article['introduction']=item.introduction
        article['date']=item.pub_date
        articles.append(article)
    categorys=get_category()
    return render(request, 'articles.html', {'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3],'categorys':categorys,'articles':articles,'prepage':prepage,'nextpage':nextpage})


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
    book['introduction']=item.introduction
    book['imgurl']=item.imgurl
    book['categorys']=item.category.split(',')
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
    article['categorys']=item.category.split(',')
    article['date']=item.pub_date
    return render(request, 'article.html',{'article':article,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def article_content(request):
    id=request.GET['id']
    item=get_article(id)
    return HttpResponse(item.content)

def categorys(request):
    try:
        key=request.GET['key']
    except:
        key=""
    try:
        page=int(request.GET['page'])
    except:
        page=1
    if page<=1:
        prepage=1
    else:
        prepage=page-1
    nextpage=page+1
    print(nextpage)
    articles=get_articles_by_category(key)
    books=get_books_by_categoty(key)
    result=[]
    lenart=len(articles[(page-1)*3:page*3])
    lenbook=len(books[(page-1)*3:page*3])
    result=articles[(page-1)*3:page*3]+books[(page-1)*3:page*3]
    if lenart<3:
        for i in range(3-lenart):
            try:
                result.append(books[page*3+i+1])
            except:
                pass
    elif lenbook<3:
        for i in range(3-lenbook):
            try:
                result.append(articles[page*3+i+1])
            except:
                pass
    items=[]
    for i in result:
        item={}
        item['title']=i.title
        item['categorys']=i.category.split(',')
        try:
            item['imgurl']=i.imgurl
            item['url']="../book?bookid=%s"%i.id
        except:
            item['url']="../article?articleid=%s"%i.id
        item['date']=i.pub_date
        item['introduction']=i.introduction[:80]+"..."
        items.append(item)
    loginvalue=islogin(request)
    categorys=get_category()
    return render(request,'categorys.html',{'items':items,'nextpage':nextpage,'prepage':prepage,'categorys':categorys,'key':key,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def userinfor(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return home(request)
    recent_books=get_books(1,6)
    recent_articles=get_articles(1,6)
    books=[]
    articles=[]
    for item in recent_books:
        book={}
        book['url']="../book?bookid=%s"%item.id
        book['title']=item.title
        book['date']=item.pub_date
        books.append(book)
    for item in recent_articles:
        article={}
        article['url']="../article?articleid=%s"%item.id
        article['title']=item.title
        article['date']=item.pub_date
        articles.append(article)
    return render(request,'user.html',{'articles':articles,'books':books,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def uploadfile(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return home(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['title'])
            return HttpResponseRedirect('/files')
    else:
        form=UploadFileForm()
    return render(request,'uploadfile.html',{'form':form,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def files(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return home(request)
    try:
        page=int(request.GET['page'])
    except:
        page=1
    if page<=1:
        prepage=1
    else:
        prepage=page-1
    nextpage=page+1
    result=get_files(page)
    files=[]
    for item in result:
        uploadfile={}
        uploadfile['title']=item.title
        uploadfile['filename']=item.filename
        uploadfile['date']=item.pub_date
        uploadfile['downloadurl']=item.downloadurl
        files.append(uploadfile)
    return render(request,'files.html',{'nextpage':nextpage,'prepage':prepage,'files':files,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})

def revisepasswd(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return home(request)
    return userinfor(request)

def sharefile(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return HttpResponseRedirect("../home")
    if request.method=='POST':
        form = ShareFileForm(request.POST)
        if form.is_valid():
            book=Book()
            book.title=form.cleaned_data['title']
            book.category=form.cleaned_data['category']
            book.imgurl=form.cleaned_data['imgurl']
            book.introduction=form.cleaned_data['introduction']
            book.downloadurl=form.cleaned_data['downloadurl']
            book.save()
            return HttpResponseRedirect("../user")
    else:
        form=ShareFileForm()
    return render(request,'sharefile.html',{'form':form,'name': loginvalue[0],'url':loginvalue[1],'class':loginvalue[2],'num':loginvalue[3]})
