# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20170331_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='password2',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
