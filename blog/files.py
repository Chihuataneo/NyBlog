from blog.models import File


def get_files(page):
    num=10
    fromnum=(page-1)*(num)
    tonum=page*(num)
    result=File.objects.order_by('-pub_date').all()[fromnum:tonum]
    return result
