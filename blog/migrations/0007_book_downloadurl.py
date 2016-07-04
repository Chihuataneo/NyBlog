# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='downloadurl',
            field=models.CharField(default=datetime.datetime(2016, 7, 4, 13, 57, 47, 91988, tzinfo=utc), max_length=256, verbose_name='downloadurl'),
            preserve_default=False,
        ),
    ]
