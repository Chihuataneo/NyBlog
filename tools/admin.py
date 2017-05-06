from django.contrib import admin
from .models import ProxyIp
# Register your models here.

class ProxyIpAdmin(admin.ModelAdmin):
    list_display=['ip','port','time']

admin.site.register(ProxyIp,ProxyIpAdmin)
