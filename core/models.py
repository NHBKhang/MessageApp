from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum


class PublicKey(models.Model):
    user = models.OneToOneField(User, related_name='public_key', on_delete=models.CASCADE, unique=True)
    key = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


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
