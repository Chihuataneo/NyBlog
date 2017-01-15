from django.contrib import admin
from .models import BoxOffice,Movie
# Register your models here.

class BoxOfficeAdmin(admin.ModelAdmin):
    list_display=['movieName','showDate','productBoxOffice']

class MovieAdmin(admin.ModelAdmin):
    list_display=['movieName','date','movie_type','plot']

admin.site.register(BoxOffice,BoxOfficeAdmin)
admin.site.register(Movie,MovieAdmin)
