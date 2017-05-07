from blog.models import File


def get_files(page):
    num = 10
    items = File.objects.order_by('-pub_date').all()[(page - 1) * (num):page * (num)]
    result = []
    for item in items:
        result.append(item.to_dict())
    return result
