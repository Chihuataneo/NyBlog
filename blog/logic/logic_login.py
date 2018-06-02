from django.contrib.auth import authenticate, login as auth_login
from blog.logic.setting import BLOGSETTING
import base64


def get_logging_status(request):
    status = {
        'username': "登录",
        'userurl': "/login",
        'btn_class_value': "button special",
        'login_state': BLOGSETTING.UNLOGGED
    }
    try:
        if request.user.is_authenticated():
            status['username'] = request.user.get_username()
            status['userurl'] = "/user"
            status['btn_class_value'] = ""
            status['login_state'] = BLOGSETTING.LOGGED
    except:
        pass
    return status


def parser_login_values(request):
    login_values = {}
    try:
        login_values['username'] = request.POST['username']
    except:
        login_values['username'] = ''
    try:
        passwd = request.POST['password']
        login_values['passwd'] = base64.b64decode(passwd)
    except:
        login_values['passwd'] = ''
    try:
        login_values['code'] = request.POST['verifycode']
    except:
        login_values['code'] = ''
    return login_values


def verify_login_values(request):
    login_values = parser_login_values(request)
    if login_values['code'] != request.session['verifycode']:
        return False
    user = authenticate(username=login_values['username'], password=login_values['passwd'])
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
        else:
            return False
    else:
        return False
