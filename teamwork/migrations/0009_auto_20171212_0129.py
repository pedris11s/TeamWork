# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0008_auto_20171212_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='para',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamwork.Estudiante'),
        ),
    ]