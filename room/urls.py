from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('room/create_room/', views.create_room, name='create_room'),
    path('room/delete_room/', views.delete_room, name='delete_room'),
]