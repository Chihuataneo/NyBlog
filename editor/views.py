from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login as auth_login,logout
from editor.models import TempArticle

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

def savearticle(request):
    loginvalue=islogin(request)
    if loginvalue[-1]==2:
        return HttpResponseRedirect("../home")
    if request.method=='POST':
        article=TempArticle()
        article.title=request.POST['title']
        article.category=request.POST['category']
        article.introduction=request.POST['description']
        article.content=request.POST['markdown']
        article.save()
        return HttpResponseRedirect("../user")
    else:
        return HttpResponseRedirect("../home")
