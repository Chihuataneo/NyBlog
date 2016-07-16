from django.db import models


class Article(models.Model):
    title = models.CharField(u'标题', max_length=256)
    category=models.CharField(u'类别',max_length=80)
    content = models.TextField(u'内容')
    introduction=models.TextField(u'简介')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable = True)
    def __str__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.title

class Book(models.Model):
    title=models.CharField("名称",max_length=256)
    category=models.CharField(u'类别',max_length=80)
    imgurl=models.CharField("imgurl",max_length=256)
    introduction=models.TextField(u'简介')
    pub_date = models.DateTimeField(u'上传时间', auto_now_add=True, editable = True)
    downloadurl=models.CharField("downloadurl",max_length=256)
    def __str__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.title

class File(models.Model):
    title=models.CharField("title",max_length=256)
    filename=models.CharField("filename",max_length=256)
    pub_date = models.DateTimeField(u'上传时间', auto_now_add=True, editable = True)
    downloadurl=models.CharField("downloadurl",max_length=256)
    def __str__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.title
