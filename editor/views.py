from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login as auth_login,logout
from blog.models import Article
from markdown2 import markdown

# Create your views here.
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

def editor(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return HttpResponseRedirect("../home")
    return render(request, 'editor.html')

def append_script(html):
    html=html+'\n<script src="../static/highlight.pack.js"></script>\n<script>hljs.initHighlightingOnLoad();</script>\n<link rel="stylesheet" href="../static/styles/solarized-dark.css" charset="utf-8">'
    return html

def publish(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return HttpResponseRedirect("../home")
    if request.method=='POST':
        article=Article()
        article.title=request.POST['title']
        article.category=request.POST['category']
        article.introduction=request.POST['description']
        html=request.POST['markdown'].replace('&nbsp;',' ').replace('\\n','\n').replace('&lt;','<').replace('&gt;','>')
        html=append_script(html)
        article.content=html
        article.save()
        return HttpResponseRedirect("../user")
    else:
        return HttpResponseRedirect("../home")
