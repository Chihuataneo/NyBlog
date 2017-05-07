from blog.models import Book


def get_books(page, num):
    items = Book.objects.order_by('-pub_date').all()[(page - 1) * num:page * num]
    result = []
    for item in items:
        item = item.to_dict()
        item['categorys'] = item['category'].split(',')
        result.append(item)
    return result


def get_book(book_id):
    book = Book.objects.filter(id=book_id)[0]
    return book


def get_books_by_category(category):
    books = Book.objects.order_by('-pub_date').all()
    result = []
    for book in books:
        if category in book.category:
            item = book.to_dict()
            item['categorys'] = item['category'].split(',')
            result.append(item)
    return result
