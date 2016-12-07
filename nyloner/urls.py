"""nyloner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','blog.views.index'),
    url(r'^home/','blog.views.home'),
    url(r'^login/','blog.views.login'),
    url(r'^blog_logout/','blog.views.blog_logout'),
    url(r'^user/','blog.views.userinfor'),
    url(r'^articles','blog.views.articles'),
    url(r'^books','blog.views.books'),
    url(r'^article','blog.views.article'),
    url(r'^book','blog.views.book'),
    url(r'^content','blog.views.article_content'),
    url(r'^categorys','blog.views.categorys'),
    url(r'^editor','editor.views.editor'),
    url(r'^revisepasswd','blog.views.revisepasswd'),
    url(r'^uploadfile','blog.views.uploadfile'),
    url(r'^files','blog.views.files'),
    url(r'^publish','editor.views.publish'),
    url(r'^sharefile','blog.views.sharefile'),
    url(r'^marks','blog.views.bookmarks'),
    url(r'^projects','blog.views.projects'),
    url(r'^verifycode','blog.views.verifycode')
]
