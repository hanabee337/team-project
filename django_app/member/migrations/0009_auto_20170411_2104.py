# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_myuser_img_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
