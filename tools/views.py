from django.shortcuts import render
import tools.movies as movies
import tools.boxoffice as bx
from django.http import HttpResponse
import json

def boxoffice(request):
    try:
        date=request.GET['date']
    except:
        return HttpResponse(content='{"status":"false"}')
    result=bx.select_by_date(date=date)
    return_data={"status":"true","movieBoxOffices":result}
    return HttpResponse(json.dumps(return_data),content_type="application/json")

def movie_detail(request):
    try:
        movie_id=request.GET['movieId']
    except:
        return HttpResponse(content='{"status":"false"}')
    result=movies.select_by_movieid(movie_id)
    return_data={"status":"true","movie":result}
    return HttpResponse(json.dumps(return_data),content_type="application/json")
