from django.contrib import admin
from .models import Article,Book
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date','introduction',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date','introduction',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Book,BookAdmin)
