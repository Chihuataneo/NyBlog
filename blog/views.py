import base64
from io import BytesIO as StringIO

from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from blog.forms import UploadFileForm, ShareFileForm
from blog.logic.logic_article import *
from blog.logic.logic_book import *
from blog.logic.logic_files import get_files
from blog.logic.logic_verify import create_verify_code
from blog.logic.logic_writefile import handle_uploaded_file
from blog.models import Book
from blog.models import File


def get_login_value(request):
    value = {
        'name': "登录",
        'url': "../login",
        'class_value': "button special",
        'state': 2
    }
    if request.user.is_authenticated():
        value['name'] = request.user.get_username()
        value['url'] = "../user"
        value['class_value'] = ""
        value['state'] = 1
    return value


def index(request):
    home_html = render_to_string('index.html')
    return HttpResponse(home_html)


def home(request):
    login_value = get_login_value(request)
    articles = get_articles(page=1, num=2)
    categorys = get_category()
    books = get_books(1, 6)
    for book in books:
        book['introduction'] = book['introduction'][:30] + "..."
    return render(request, 'home.html',
                  {'name': login_value['name'], 'url': login_value['url'], 'class': login_value['class_value'],
                   'num': login_value['state'], 'articles': articles, 'categorys': categorys, 'books': books})


def login_GET(request):
    login_value = get_login_value(request)
    login_html = render_to_string('login.html')
    return render(request, 'login.html',
                  {'name': login_value['name'], 'url': login_value['url'], 'class': login_value['class_value'],
                   'num': login_value['state']})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        passwd = base64.b64decode(passwd)
        code = request.POST['verifycode']
        if code != request.session['verifycode']:
            return login_GET(request)
        user = authenticate(username=username, password=passwd)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return userinfor(request)
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
    login_value = get_login_value(request)
    try:
        page = int(request.GET['page'])
        num = int(request.GET['num'])
    except:
        page = 1
        num = 6
    if page <= 1:
        prepage = 1
    else:
        prepage = page - 1
    nextpage = page + 1
    books = get_books(page, num)
    for book in books:
        book['introduction'] = book['introduction'][:80] + "..."
    categorys = get_category()
    recent_books = get_books(1, 4)
    recent_articles = get_articles(1, 4)
    return render(request, 'books.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'name': login_value['name'],
                   'url': login_value['url'], 'class': login_value['class_value'], 'num': login_value['state'],
                   'categorys': categorys, 'books': books, 'prepage': prepage, 'nextpage': nextpage})


def articles(request):
    login_value = get_login_value(request)
    try:
        page = int(request.GET['page'])
        num = int(request.GET['num'])
    except:
        page = 1
        num = 6
    if page <= 1:
        prepage = 1
    else:
        prepage = page - 1
    nextpage = page + 1
    articles = get_articles(page, num)
    categorys = get_category()
    recent_books = get_books(1, 4)
    recent_articles = get_articles(1, 4)
    return render(request, 'articles.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'name': login_value['name'],
                   'url': login_value['url'], 'class': login_value['class_value'], 'num': login_value['state'],
                   'categorys': categorys, 'articles': articles, 'prepage': prepage, 'nextpage': nextpage})


def book(request):
    try:
        bookid = request.GET['bookid']
        bookid = int(bookid)
    except:
        return books(request)
    login_value = get_login_value(request)
    item = get_book(bookid)
    item.number += 1
    item.save()
    book = item.to_dict()
    return render(request, 'book.html', {'book': book, 'name': login_value['name'], 'url': login_value['url'],
                                         'class': login_value['class_value'], 'num': login_value['state']})


def article(request):
    try:
        articleid = request.GET['articleid']
    except:
        return articles(request)
    login_value = get_login_value(request)
    item = get_article(articleid)
    article = item.to_dict()
    return render(request, 'article.html', {'article': article, 'name': login_value['name'], 'url': login_value['url'],
                                            'class': login_value['class_value'], 'num': login_value['state']})


def article_content(request):
    id = request.GET['id']
    item = get_article(id)
    item.number += 1
    item.save()
    return HttpResponse(item.content)


def categorys(request):
    try:
        key = request.GET['key']
    except:
        key = ""
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    if page <= 1:
        prepage = 1
    else:
        prepage = page - 1
    nextpage = page + 1
    articles = get_articles_by_category(key)
    books = get_books_by_category(key)
    lenart = len(articles[(page - 1) * 3:page * 3])
    lenbook = len(books[(page - 1) * 3:page * 3])
    result = articles[(page - 1) * 3:page * 3] + books[(page - 1) * 3:page * 3]
    if lenart < 3:
        for i in range(3 - lenart):
            try:
                result.append(books[page * 3 + i + 1])
            except:
                pass
    elif lenbook < 3:
        for i in range(3 - lenbook):
            try:
                result.append(articles[page * 3 + i + 1])
            except:
                pass
    items = []
    for item in result:
        if 'imgurl' in item:
            item['url'] = "../book?bookid=%s" % item['id']
        else:
            item['url'] = "../article?articleid=%s" % item['id']
        item['introduction'] = item['introduction'][:80] + "..."
        items.append(item)
    login_value = get_login_value(request)
    categorys = get_category()
    recent_books = get_books(1, 4)
    recent_articles = get_articles(1, 4)
    return render(request, 'categorys.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'items': items,
                   'nextpage': nextpage, 'prepage': prepage, 'categorys': categorys, 'key': key,
                   'name': login_value['name'], 'url': login_value['url'], 'class': login_value['class_value'],
                   'num': login_value['state']})


def userinfor(request):
    login_value = get_login_value(request)
    if login_value['state'] == 2:
        return home(request)
    books = get_books(1, 6)
    articles = get_articles(1, 6)
    return render(request, 'user.html',
                  {'articles': articles, 'books': books, 'name': login_value['name'], 'url': login_value['url'],
                   'class': login_value['class_value'], 'num': login_value['state']})


def uploadfile(request):
    login_value = get_login_value(request)
    if login_value['state'] == 2:
        return home(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            return HttpResponseRedirect('/files')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfile.html', {'form': form, 'name': login_value['name'], 'url': login_value['url'],
                                               'class': login_value['class_value'], 'num': login_value['state']})


def files(request):
    login_value = get_login_value(request)
    if login_value['state'] == 2:
        return home(request)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    if page <= 1:
        prepage = 1
    else:
        prepage = page - 1
    nextpage = page + 1
    files = get_files(page)
    return render(request, 'files.html',
                  {'nextpage': nextpage, 'prepage': prepage, 'files': files, 'name': login_value['name'],
                   'url': login_value['url'], 'class': login_value['class_value'], 'num': login_value['state']})


def delete(request):
    try:
        filename = request.GET['filename']
    except:
        return files(request)
    File.objects.filter(filename=filename).delete()
    try:
        import os
        os.remove('collected_static/files/%s' % filename)
    except:
        pass
    return files(request)


def revisepasswd(request):
    login_value = get_login_value(request)
    if login_value['state'] == 2:
        return home(request)
    return userinfor(request)


def sharefile(request):
    login_value = get_login_value(request)
    if login_value['state'] == 2:
        return HttpResponseRedirect("../home")
    if request.method == 'POST':
        form = ShareFileForm(request.POST)
        if form.is_valid():
            book = Book()
            book.title = form.cleaned_data['title']
            book.category = form.cleaned_data['category']
            book.imgurl = form.cleaned_data['imgurl']
            book.introduction = form.cleaned_data['introduction']
            book.downloadurl = form.cleaned_data['downloadurl']
            book.save()
            return HttpResponseRedirect("../user")
    else:
        form = ShareFileForm()
    return render(request, 'sharefile.html', {'form': form, 'name': login_value['name'], 'url': login_value['url'],
                                              'class': login_value['class_value'], 'num': login_value['state']})


def bookmarks(request):
    login_value = get_login_value(request)
    return render(request, 'bookmarks.html',
                  {'name': login_value['name'], 'url': login_value['url'], 'class': login_value['class_value'],
                   'num': login_value['state']})


def projects(request):
    login_value = get_login_value(request)
    return render(request, 'projects.html',
                  {'name': login_value['name'], 'url': login_value['url'], 'class': login_value['class_value'],
                   'num': login_value['state']})


def verifycode(request):
    try:
        input_code = request.GET['inputcode']
        if str(input_code) != request.session['verifycode']:
            return HttpResponse('False')
        else:
            return HttpResponse('True')
    except:
        pass
    img, code = create_verify_code()
    mstream = StringIO()
    request.session['verifycode'] = code
    img.save(mstream, "jpeg")
    return HttpResponse(mstream.getvalue(), content_type="image/jpeg")
