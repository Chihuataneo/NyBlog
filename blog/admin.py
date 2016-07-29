from django.contrib import admin
from .models import Article,Book,File
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','number','pub_date','introduction',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title','category','number','pub_date','introduction',)

class FilesAdmin(admin.ModelAdmin):
    list_display=('title','filename','pub_date','downloadurl',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(File,FilesAdmin)
