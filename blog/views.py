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
from blog.logic.logic_tools import get_tools
from blog.logic.setting import BLOGSETTING


def get_logging_status(request):
    status = {
        'name': "登录",
        'url': "/login",
        'class_value': "button special",
        'state': BLOGSETTING.UNLOGGED
    }
    if request.user.is_authenticated():
        status['name'] = request.user.get_username()
        status['url'] = "/user"
        status['class_value'] = ""
        status['state'] = BLOGSETTING.LOGGED
    return status


def index(request):
    home_html = render_to_string('index.html')
    return HttpResponse(home_html)


def home(request):
    logging_status = get_logging_status(request)
    articles = get_articles(page=1, num=2)
    categorys = get_category()
    books = get_books(1, 6)
    for book in books:
        book['introduction'] = book['introduction'][:60] + "..."
    return render(request, 'home.html',
                  {'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'],
                   'num': logging_status['state'], 'articles': articles, 'categorys': categorys, 'books': books})


def login_GET(request):
    logging_status = get_logging_status(request)
    return render(request, 'login.html',
                  {'tools': get_tools(), 'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'],
                   'num': logging_status['state']})


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
    logging_status = get_logging_status(request)
    try:
        page = int(request.GET['page'])
        num = int(request.GET['num'])
    except:
        page = 1
        num = 6
    if page <= 1:
        last_page = 1
    else:
        last_page = page - 1
    books = get_books(page, num)
    next_page = page + 1
    if len(books) < num:
        next_page = page
    for book in books:
        book['introduction'] = book['introduction'][:80] + "..."

    categorys = get_category()
    recent_books = get_recent_books(4)
    recent_articles = get_recent_articles(4)
    return render(request, 'books.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'tools': get_tools(),
                   'tools': get_tools(), 'name': logging_status['name'],
                   'url': logging_status['url'], 'class': logging_status['class_value'], 'num': logging_status['state'],
                   'categorys': categorys, 'books': books, 'last_page': last_page, 'next_page': next_page})


def articles(request):
    logging_status = get_logging_status(request)
    try:
        page = int(request.GET['page'])
        num = int(request.GET['num'])
    except:
        page = 1
        num = 6
    if page <= 1:
        last_page = 1
    else:
        last_page = page - 1
    articles = get_articles(page, num)
    if len(articles) < num:
        next_page = page
    else:
        next_page = page + 1
    categorys = get_category()

    recent_books = get_recent_books(4)
    recent_articles = get_recent_articles(4)

    return render(request, 'articles.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'tools': get_tools(),
                   'tools': get_tools(), 'name': logging_status['name'],
                   'url': logging_status['url'], 'class': logging_status['class_value'], 'num': logging_status['state'],
                   'categorys': categorys, 'articles': articles, 'last_page': last_page, 'next_page': next_page})


def book(request):
    try:
        book_id = request.GET['bookid']
    except:
        return books(request)
    logging_status = get_logging_status(request)
    item = get_book(book_id)
    item.number += 1
    item.save()
    book_dict = item.to_dict()
    book_dict['categorys'] = book_dict['category'].split(',')
    return render(request, 'book.html',
                  {'book': book_dict, 'tools': get_tools(), 'tools': get_tools(), 'name': logging_status['name'],
                   'url': logging_status['url'],
                   'class': logging_status['class_value'], 'num': logging_status['state']})


def article(request):
    try:
        article_id = request.GET['articleid']
    except:
        return articles(request)
    logging_status = get_logging_status(request)
    item = get_article(article_id)
    article_dict = item.to_dict()
    article_dict['categorys'] = article_dict['category'].split(',')
    return render(request, 'article.html',
                  {'article': article_dict, 'tools': get_tools(), 'tools': get_tools(), 'name': logging_status['name'],
                   'url': logging_status['url'],
                   'class': logging_status['class_value'], 'num': logging_status['state']})


def article_content(request):
    article_id = request.GET['id']
    item = get_article(article_id)
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
        last_page = 1
    else:
        last_page = page - 1
    next_page = page + 1
    articles = get_articles_by_category(key)
    books = get_books_by_category(key)
    len_of_articles = len(articles[(page - 1) * 3:page * 3])
    len_of_books = len(books[(page - 1) * 3:page * 3])
    result = articles[(page - 1) * 3:page * 3] + books[(page - 1) * 3:page * 3]
    if len_of_articles < 3:
        for i in range(3 - len_of_articles):
            try:
                result.append(books[page * 3 + i + 1])
            except:
                pass
    elif len_of_books < 3:
        for i in range(3 - len_of_books):
            try:
                result.append(articles[page * 3 + i + 1])
            except:
                pass
    if len(result) < 6:
        next_page = page
    items = []
    for item in result:
        if 'imgurl' in item:
            item['url'] = "/book?bookid=%s" % item['id']
        else:
            item['url'] = "/article?articleid=%s" % item['id']
        item['introduction'] = item['introduction'][:80] + "..."
        items.append(item)
    logging_status = get_logging_status(request)

    categorys = get_category()
    recent_books = get_recent_books(4)
    recent_articles = get_recent_articles(4)
    return render(request, 'categorys.html',
                  {'recent_books': recent_books, 'recent_articles': recent_articles, 'items': items,
                   'next_page': next_page, 'last_page': last_page, 'categorys': categorys, 'key': key,
                   'tools': get_tools(), 'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'],
                   'num': logging_status['state']})


def userinfor(request):
    logging_status = get_logging_status(request)
    if logging_status['state'] == BLOGSETTING.UNLOGGED:
        return home(request)

    books = get_recent_books(6)
    articles = get_recent_articles(6)

    return render(request, 'user.html',
                  {'articles': articles, 'books': books, 'tools': get_tools(), 'name': logging_status['name'],
                   'url': logging_status['url'],
                   'class': logging_status['class_value'], 'num': logging_status['state']})


def uploadfile(request):
    logging_status = get_logging_status(request)
    if logging_status['state'] == BLOGSETTING.UNLOGGED:
        return home(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            return HttpResponseRedirect('/files')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfile.html',
                  {'form': form, 'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'], 'num': logging_status['state']})


def files(request):
    logging_status = get_logging_status(request)
    if logging_status['state'] == BLOGSETTING.UNLOGGED:
        return home(request)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    if page <= 1:
        last_page = 1
    else:
        last_page = page - 1
    next_page = page + 1
    files = get_files(page)
    return render(request, 'files.html',
                  {'next_page': next_page, 'last_page': last_page, 'files': files, 'tools': get_tools(),
                   'name': logging_status['name'],
                   'url': logging_status['url'], 'class': logging_status['class_value'], 'num': logging_status['state']})


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
    logging_status = get_logging_status(request)
    if logging_status['state'] == BLOGSETTING.UNLOGGED:
        return home(request)
    return userinfor(request)


def sharefile(request):
    logging_status = get_logging_status(request)
    if logging_status['state'] == BLOGSETTING.UNLOGGED:
        return HttpResponseRedirect("/home")
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
            return HttpResponseRedirect("/user")
    else:
        form = ShareFileForm()
    return render(request, 'sharefile.html',
                  {'form': form, 'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'], 'num': logging_status['state']})


def bookmarks(request):
    logging_status = get_logging_status(request)
    return render(request, 'bookmarks.html',
                  {'tools': get_tools(), 'name': logging_status['name'], 'url': logging_status['url'],
                   'class': logging_status['class_value'],
                   'num': logging_status['state']})


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
