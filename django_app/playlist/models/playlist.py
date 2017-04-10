from django.conf import settings
from django.db import models

__all__ = (
    'PlayList',
    # 'PlayListMusic',
)

class PlayList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    # playlist_music = models.ManyToManyField(
    #     'music.Music',
    #     blank=True,
    #     through='PlayListMusic',
    #     related_name='music_playlist_set'
    # )

    class Meta:
        ordering = ('-pk',)


# class PlayListMusic(models.Model):
#     playlist = models.ForeignKey(PlayList)
#     music = models.ForeignKey('music.Music')
#     created_date = models.DateTimeField(auto_now_add=True)
