from django.shortcuts import render
from django.http import HttpResponseRedirect
from blog.models import Article
from blog.logic.logic_login import get_logging_status
from blog.logic.setting import BLOGSETTING


def editor(request):
    logging_status = get_logging_status(request)
    if logging_status['login_state'] == BLOGSETTING.UNLOGGED:
        return HttpResponseRedirect("../home")
    return render(request, 'editor.html')


def append_script(html):
    html = html + '\n<script src="../static/highlight.pack.js"></script>\n<script>hljs.initHighlightingOnLoad();</script>\n<link rel="stylesheet" href="../static/styles/atom-one-dark.css" charset="utf-8">'
    return html


def publish(request):
    logging_status = get_logging_status(request)
    if logging_status['login_state'] == BLOGSETTING.UNLOGGED:
        return HttpResponseRedirect("../home")
    if request.method == 'POST':
        article = Article()
        article.title = request.POST['title']
        article.category = request.POST['category']
        article.introduction = request.POST['description']
        html = request.POST['html'].replace('&nbsp;', ' ').replace('\\n', '\n') \
            .replace('&lt;', '<').replace('&gt;', '>')
        html = append_script(html)

        markdown = request.POST['markdown'].replace('&nbsp;', ' ').replace('\\n', '\n') \
            .replace('&lt;', '<').replace('&gt;', '>')
        article.markdown = markdown
        article.content = html
        article.save()
        return HttpResponseRedirect("../user")
    else:
        return HttpResponseRedirect("../home")
