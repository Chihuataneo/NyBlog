from django.contrib import admin
from editor.models import TempArticle
# Register your models here.
class TempArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date','introduction',)


admin.site.register(TempArticle,TempArticleAdmin)
