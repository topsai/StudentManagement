# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_auto_20170705_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='menu',
            field=models.ManyToManyField(related_name='au', to='myadmin.Menu'),
        ),
    ]
