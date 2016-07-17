from django.db import models

# Create your models here.
class TempArticle(models.Model):
    title = models.CharField(u'标题', max_length=256)
    category=models.CharField(u'类别',max_length=80)
    content = models.TextField(u'内容')
    introduction=models.TextField(u'简介')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable = True)
    def __str__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.title
