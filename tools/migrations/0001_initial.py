# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoxOffice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('movieId', models.IntegerField(verbose_name='movieId')),
                ('movieName', models.CharField(verbose_name='movieName', max_length=80)),
                ('movieNameEnglish', models.CharField(verbose_name='movieNameEnglish', max_length=80)),
                ('releaseDate', models.CharField(verbose_name='releaseDate', max_length=80)),
                ('showDate', models.CharField(verbose_name='showDate', max_length=80)),
                ('productBoxOffice', models.FloatField(verbose_name='productBoxOffice')),
                ('productTotalBoxOffice', models.FloatField(verbose_name='productTotalBoxOffice')),
                ('productBoxOfficeRate', models.FloatField(verbose_name='productBoxOfficeRate')),
                ('productScheduleRate', models.FloatField(verbose_name='productScheduleRate')),
                ('productTicketSeatRate', models.FloatField(verbose_name='productTicketSeatRate')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movieId', models.IntegerField(primary_key=True, verbose_name='movieId', serialize=False)),
                ('movieName', models.CharField(verbose_name='movieName', max_length=80)),
                ('pictureUrl', models.CharField(verbose_name='pictureUrl', max_length=255)),
                ('date', models.CharField(verbose_name='date', max_length=30)),
                ('director', models.CharField(verbose_name='date', max_length=80)),
                ('actors', models.CharField(verbose_name='actors', max_length=255)),
                ('plot', models.CharField(verbose_name='plot', max_length=512)),
                ('score', models.FloatField(verbose_name='score')),
                ('time_length', models.CharField(verbose_name='time', max_length=20)),
                ('movie_type', models.CharField(verbose_name='type', max_length=80)),
            ],
        ),
    ]
