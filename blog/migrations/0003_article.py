# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='标题', max_length=256)),
                ('category', models.CharField(verbose_name='类别', max_length=80)),
                ('content', models.TextField(verbose_name='内容')),
                ('introduction', models.TextField(verbose_name='简介')),
                ('pub_date', models.DateTimeField(verbose_name='发表时间', auto_now_add=True)),
            ],
        ),
    ]
