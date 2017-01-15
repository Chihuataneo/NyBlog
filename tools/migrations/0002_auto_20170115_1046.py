# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxoffice',
            name='movieId',
            field=models.CharField(verbose_name='movieId', max_length=10),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movieId',
            field=models.CharField(serialize=False, verbose_name='movieId', max_length=10, primary_key=True),
        ),
    ]
