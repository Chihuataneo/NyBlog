from .models import Movie

def select_by_movieid(movie_id):
    rows=Movie.objects.filter(movieId=movie_id)
    try:
        result=rows[0].to_dict()
    except:
        result={}
    return result

def select_by_name(movie_name):
    result=Movie.objects.filter(movieName=movie_name)
    return result
