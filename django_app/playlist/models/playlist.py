from django.conf import settings
from django.db import models

from search.models import Music

__all__ = (
    'PlayList',
    'PlayListMusic',
    'PlayListLikeUser',
)


class PlayList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    like_user_count = models.IntegerField(blank=True, default=0)
    playlist_music = models.ManyToManyField(
        Music,
        blank=True,
        through='PlayListMusic',
        related_name='music_playlist_set'
    )
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        through='PlayListLikeUser',
        related_name='user_like_playlist'
    )

    class Meta:
        ordering = ('-pk',)


class PlayListMusic(models.Model):
    playlist = models.ForeignKey(PlayList)
    music = models.ForeignKey(Music)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'music')


class PlayListLikeUser(models.Model):
    playlist = models.ForeignKey(PlayList)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'user')
