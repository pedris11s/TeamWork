# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-04 14:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0018_auto_20171222_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField(default=datetime.date.today)),
                ('visitas', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 16, 41, 55, 880622)),
        ),
    ]