# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zumaInfo', '0003_auto_20170511_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajador',
            name='descripcion',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='cantidad_votos',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='valoracion',
            field=models.IntegerField(default=5),
        ),
    ]
