from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from crypto import aes
import secrets


class SecretKey(models.Model):
    key = models.CharField(max_length=256, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(16)
        return super().save(*args, **kwargs)

    class Meta:
        managed = False


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    key = models.ForeignKey(SecretKey, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.key = SecretKey.objects.create()
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
