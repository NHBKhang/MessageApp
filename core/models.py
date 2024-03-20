from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum


class PublicKey(models.Model):
    user = models.OneToOneField(User, related_name='public_key', on_delete=models.CASCADE, unique=True)
    key = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=15, null=True)
    gender = enum.EnumField(Gender, default=Gender.MALE, null=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=128, null=True)
    avatar = models.ImageField(upload_to='profile_pics', null=True)
    description = models.TextField(null=True, blank=True)


class NotificationType(enum.Enum):
    Error = 0
    KeypairError = 1
    NoKeypairError = 2
    PrivateKeyError = 3
    PublicKeyError = 4


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    type = enum.EnumField(NotificationType, default=NotificationType.Error)
    is_read = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
