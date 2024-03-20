from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from crypto import chacha20
import secrets


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    key = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = chacha20.generate_key()
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_key(self):
        return chacha20.base64_to_bytes(self.key)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    nonce = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        if self.nonce:
            self.nonce = chacha20.bytes_to_base64(self.nonce)
        return super().save(*args, **kwargs)

    def get_nonce(self):
        return chacha20.base64_to_bytes(self.nonce)

    class Meta:
        ordering = ('date_added',)
