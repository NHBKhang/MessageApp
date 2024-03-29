from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message


@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    for message in messages:
        from crypto import chacha20
        message.content = chacha20.decrypt(key=room.get_key(), cipher_message=message.content, nonce=message.get_nonce())

    return render(request, 'room/room.html', {'room': room, 'messages': messages})


@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            room = Room.objects.create(name=name)

            return redirect('room', slug=room.slug)


@login_required
def delete_room(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id:
            Room.objects.get(pk=int(id)).delete()

    return redirect('rooms')
