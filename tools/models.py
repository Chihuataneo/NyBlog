from django.db import models

# Create your models here.
class BoxOffice(models.Model):
    movieId=models.CharField("movieId",max_length=10)
    movieName=models.CharField("movieName",max_length=80)
    movieNameEnglish=models.CharField("movieNameEnglish",max_length=80)
    releaseDate=models.CharField("releaseDate",max_length=80)
    showDate=models.CharField("showDate",max_length=80)
    productBoxOffice=models.FloatField("productBoxOffice")
    productTotalBoxOffice=models.FloatField("productTotalBoxOffice")
    productBoxOfficeRate=models.FloatField("productBoxOfficeRate")
    productScheduleRate=models.FloatField("productScheduleRate")
    productTicketSeatRate=models.FloatField("productTicketSeatRate")
    def __str__(self):
        return self.movieName

    def to_dict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class Movie(models.Model):
    movieId=models.CharField("movieId",primary_key=True,max_length=10)
    movieName=models.CharField("movieName",max_length=80)
    pictureUrl=models.CharField("pictureUrl",max_length=255)
    date=models.CharField("date",max_length=30)
    director=models.CharField("date",max_length=80)
    actors=models.CharField("actors",max_length=255)
    plot=models.TextField("plot")
    score=models.FloatField("score")
    time_length=models.CharField("time",max_length=20)
    movie_type=models.CharField("type",max_length=80)
    def __str__(self):
        return self.movieName
    def to_dict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
