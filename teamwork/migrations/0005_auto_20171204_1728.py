# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0004_auto_20171130_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='integrantes',
            field=models.ManyToManyField(related_name='integrantes', to='teamwork.Estudiante'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='jefe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jefe', to='teamwork.Estudiante'),
        ),
    ]
