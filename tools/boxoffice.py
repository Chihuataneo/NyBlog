from .models import BoxOffice


def select_by_date(date="2017-01-01"):
    rows=BoxOffice.objects.filter(showDate=date)
    result=[]
    for row in rows:
        result.append(row.to_dict())
    return result

def select_by_movieid(movie_id):
    rows=BoxOffice.objects.filter(movieId=movie_id)
    result=[]
    for row in rows:
        result.append(row.to_dict())
    return result

def select_by_name(movie_name):
    rows=BoxOffice.objects.filter(movieName=movie_name)
    result=[]
    for row in rows:
        result.append(row.to_dict())
    return result
