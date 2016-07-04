# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='名称', max_length=256)),
                ('category', models.CharField(verbose_name='类别', max_length=80)),
                ('imgurl', models.CharField(verbose_name='imgurl', max_length=256)),
                ('introduction', models.TextField(verbose_name='简介')),
                ('pub_date', models.DateTimeField(verbose_name='上传时间', auto_now_add=True)),
            ],
        ),
    ]
