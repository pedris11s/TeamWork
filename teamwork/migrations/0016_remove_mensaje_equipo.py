# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 19:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0015_mensaje'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='equipo',
        ),
    ]