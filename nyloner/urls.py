"""nyloner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home))
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home))
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog import views as blog_views
from tools import views as tools_views
from editor import views as editor_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', blog_views.index),
    url(r'^home/', blog_views.home),
    url(r'^login/', blog_views.login),
    url(r'^blog_logout/', blog_views.blog_logout),
    url(r'^user/', blog_views.userinfor),
    url(r'^articles', blog_views.articles),
    url(r'^books', blog_views.books),
    url(r'^article', blog_views.article),
    url(r'^book', blog_views.book),
    url(r'^content', blog_views.article_content),
    url(r'^categorys', blog_views.categorys),
    url(r'^revisepasswd', blog_views.revisepasswd),
    url(r'^uploadfile', blog_views.uploadfile),
    url(r'^files', blog_views.files),
    url(r'^sharefile', blog_views.sharefile),
    url(r'^marks', blog_views.bookmarks),
    url(r'^verifycode', blog_views.verifycode),
    url(r'^delete', blog_views.delete),
    url(r'about',blog_views.about),

    url(r'^editor', editor_views.editor),
    url(r'^publish', editor_views.publish),

    url(r'^proxy', tools_views.proxy),
    url(r'^tools', tools_views.tools),
    url(r'^coder', tools_views.coder),
    url(r'^ipinfo', tools_views.tool_ip_query),
]
