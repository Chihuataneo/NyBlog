from blog.models import File


def get_files(page):
    num=10
    fromnum=(page-1)*(num)
    tonum=page*(num)
    items=File.objects.order_by('-pub_date').all()[fromnum:tonum]
    result=[]
    for item in items:
        result.append(item.to_dict())
    return result
