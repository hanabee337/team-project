from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class MyUser(AbstractUser):
    pass
    # user_playlist = models.ManyToManyField(
    #     'playlist.PlayList',
    #     blank=True,
    #     through='UserPlayList',
    #     related_name='playlist_user_set'
    # )
#
#
# class UserPlayList(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     playlist = models.ForeignKey('playlist.PlayList')
#     created_date = models.DateTimeField(auto_now_add=True)
#

