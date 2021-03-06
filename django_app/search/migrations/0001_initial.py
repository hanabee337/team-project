# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.CharField(max_length=255)),
                ('rank', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('artist', models.TextField(max_length=255)),
                ('preview', models.TextField(max_length=500)),
                ('artist_picture_small', models.TextField(max_length=500)),
                ('artist_picture_medium', models.TextField(max_length=500)),
                ('artist_picture_big', models.TextField(max_length=500)),
                ('album_id', models.CharField(max_length=255)),
                ('album_title', models.CharField(max_length=255)),
                ('album_picture_small', models.TextField(max_length=500)),
                ('album_picture_medium', models.TextField(max_length=500)),
                ('album_picture_big', models.TextField(max_length=500)),
            ],
        ),
    ]
