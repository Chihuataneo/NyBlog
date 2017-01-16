from django.contrib import admin
from .models import BoxOffice,Movie,ProxyIp
# Register your models here.

class BoxOfficeAdmin(admin.ModelAdmin):
    list_display=['movieName','showDate','productBoxOffice']

class MovieAdmin(admin.ModelAdmin):
    list_display=['movieName','date','movie_type','plot']

class ProxyIpAdmin(admin.ModelAdmin):
    list_display=['ip','port','time']

admin.site.register(BoxOffice,BoxOfficeAdmin)
admin.site.register(Movie,MovieAdmin)
admin.site.register(ProxyIp,ProxyIpAdmin)
