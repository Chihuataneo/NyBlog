from blog.models import Article
from blog.models import Book


def get_articles(page, num):
    items = Article.objects.order_by('-pub_date').all()[(page - 1) * num:page * num]
    result = []
    for item in items:
        result.append(item.to_dict())
    return result


def get_article(article_id):
    article = Article.objects.filter(id=article_id)[0]
    return article


def get_articles_by_category(category):
    articles = Article.objects.order_by('-pub_date').all()
    result = []
    for item in articles:
        if category in item.category:
            result.append(item.to_dict())
    return result


def get_category():
    result = {}
    for item in Article.objects.all():
        try:
            keys = item.category.split(',')
        except:
            continue
        for key in keys:
            try:
                result[key] += 2
            except:
                result[key] = 10
    for item in Book.objects.all():
        try:
            keys = item.category.split(',')
        except:
            continue
        for key in keys:
            try:
                result[key] += 2
            except:
                result[key] = 10
    return result
