from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models


class MyUser(AbstractUser):
    CHOICES_GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30)
    email = models.EmailField(blank=False, null=False)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    age = models.IntegerField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
