# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 13:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_auto_20170705_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': '菜单', 'verbose_name_plural': '菜单'},
        ),
    ]