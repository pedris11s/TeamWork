# Generated by Django 2.1.1 on 2018-09-30 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0022_auto_20180929_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 29, 20, 46, 27, 740492)),
        ),
    ]