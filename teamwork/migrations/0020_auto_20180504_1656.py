# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-04 14:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0019_auto_20180504_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 16, 56, 17, 526632)),
        ),
    ]
