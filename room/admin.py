from django.contrib import admin

from .models import Room
from .forms import RoomForm


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm


admin.site.register(Room, RoomAdmin)
