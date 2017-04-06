# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 23:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='PlayListMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.PlayList')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_music',
            field=models.ManyToManyField(blank=True, related_name='music_playlist_set', through='playlist.PlayListMusic', to='music.Music'),
        ),
    ]
