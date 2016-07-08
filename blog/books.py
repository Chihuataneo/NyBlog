from blog.models import Book


def get_books(page,num):
    fromnum=(page-1)*(num-1)
    tonum=page*(num)
    result=Book.objects.order_by('-pub_date').all()[fromnum:tonum]
    return result

def get_book(bookid):
    book=Book.objects.filter(id=bookid)[0]
    return book

def get_books_by_categoty(category):
    books=Book.objects.order_by('-pub_date').all()
    result=[]
    for book in books:
        if category in book.category:
            result.append(book)
    return result
