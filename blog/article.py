from blog.models import Article
from blog.models import Book

def get_articles(page,num):
    fromnum=(page-1)*(num-1)
    tonum=page*(num)
    result=Article.objects.order_by('-pub_date').all()[fromnum:tonum]
    return result

def get_article(articleid):
    article=Article.objects.filter(id=articleid)[0]
    return article

def get_category():
    result={}
    for item in Article.objects.all():
        try:
            keys=item.category.split(',')
        except:
            continue
        for key in keys:
            try:
                result[key]+=2
            except:
                result[key]=10
    for item in Book.objects.all():
        try:
            keys=item.category.split(',')
        except:
            continue
        for key in keys:
            try:
                result[key]+=2
            except:
                result[key]=10
    return result
