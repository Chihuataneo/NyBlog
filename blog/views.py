from django.shortcuts import render
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login as auth_login,logout
import base64

# Create your views here.
def index(request):
    home_html=render_to_string('index.html')
    return HttpResponse(home_html)

def home(request):
    buttontext="登录"
    url="../login"
    classvalue="button special"
    num=2
    if request.user.is_authenticated():
        buttontext=request.user.get_username()
        url="../userinfor"
        classvalue=""
        num=1
    return render(request, 'home.html', {'name': buttontext,'url':url,'class':classvalue,'num':num})

def login(request):
    if request.method=='GET':
        login_html=render_to_string('login.html')
        return HttpResponse(login_html)
    else:
        username=request.POST['username']
        passwd=request.POST['password']
        passwd=base64.b64decode(passwd)
        user=authenticate(username=username,password=passwd)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return home(request)
            else:
                login_html=render_to_string('login.html')
                return HttpResponse(login_html)
        else:
            login_html=render_to_string('login.html')
            return HttpResponse(login_html)

def blog_logout(request):
    logout(request)
    return home(request)

def userinfor(request):
    return home(request)
