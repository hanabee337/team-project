from django.conf import settings
from django.db import models

from search.models import Music

__all__ = (
    'PlayList',
    'PlayListMusic',
)


class PlayList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    playlist_music = models.ManyToManyField(
        Music,
        blank=True,
        through='PlayListMusic',
        related_name='music_playlist_set'
    )

    class Meta:
        ordering = ('-pk',)


class PlayListMusic(models.Model):
    playlist = models.ForeignKey(PlayList)
    music = models.ForeignKey(Music)
    created_date = models.DateTimeField(auto_now_add=True)

