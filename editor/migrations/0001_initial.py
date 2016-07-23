# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('category', models.CharField(max_length=80, verbose_name='类别')),
                ('content', models.TextField(verbose_name='内容')),
                ('introduction', models.TextField(verbose_name='简介')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
            ],
        ),
    ]
