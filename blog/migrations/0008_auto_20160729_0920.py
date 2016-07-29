# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_book_downloadurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('filename', models.CharField(max_length=256, verbose_name='filename')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('downloadurl', models.CharField(max_length=256, verbose_name='downloadurl')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='number',
            field=models.IntegerField(verbose_name='阅读人数', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.IntegerField(verbose_name='阅读人数', default=0),
            preserve_default=False,
        ),
    ]
