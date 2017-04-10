from django.db import models


class Music(models.Model):
    artist = models.TextField(max_length=255)
    title = models.CharField(max_length=255)
    preview = models.TextField(max_length=500)
    artist_picture = models.TextField(max_length=500)
    album_picture = models.TextField(max_length=500)


    def __str__(self):
        return self.title
