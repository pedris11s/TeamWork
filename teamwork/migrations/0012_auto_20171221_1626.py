# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0011_auto_20171219_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='avatar',
            field=models.ImageField(upload_to='teamwork/static'),
        ),
    ]