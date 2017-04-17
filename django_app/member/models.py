from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def _create_user(self, nickname, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        # username을 email로(email을 user id로 사용)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, nickname=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, email, password, **extra_fields)

    def create_superuser(self, nickname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(nickname, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    CHOICES_GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    CHOICES_USER_TYPE = (
        ('D', 'Django'),
        ('F', 'Facebook'),
    )

    # username = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER, default='M')
    age = models.IntegerField(blank=True, null=True)
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE, default='D')
    is_staff = models.BooleanField(default=False)

    # password1 = models.CharField(max_length=255)
    # password2 = models.CharField(max_length=255)

    img_profile = models.ImageField(upload_to='user', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
