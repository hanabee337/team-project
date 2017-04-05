from django.db import models


# Create your models here.


class PlayList(models.Model):
    title = models.CharField(max_length=100)
    # published_date = models.DateTimeField()
    playlist_music = models.ManyToManyField(
        'video.Video',
        blank=True,
        through='PlayListMusic',
        related_name='music_playlist_set'
    )

    def __str__(self):
        return self.title


class PlayListMusic(models.Model):
    playlist = models.ForeignKey('playlist.PlayList')
    music = models.ForeignKey('video.Video')
    created_date = models.DateTimeField(auto_now_add=True)
