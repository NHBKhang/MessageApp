import json
from djangochat import settings
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, Message
from crypto import rsa


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        if message != '':
            await self.save_message(username, room, message)

        from core.models import PublicKey
        get_public_key = sync_to_async(PublicKey.objects.get)

        # Gọi hàm trong ngữ cảnh bất đồng bộ
        key = await get_public_key(user_id=10)

        if key != '':
            # encrypt message using user public key
            message = rsa.encrypt(message, rsa.string_to_public_key(key.key))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        private_key = rsa.read_private_key(username)
        if private_key:
            message = rsa.decrypt(message, private_key)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        from crypto import chacha20
        nonce = chacha20.generate_nonce()
        message = chacha20.encrypt(message=message, nonce=nonce, key=room.get_key())

        Message.objects.create(user=user, room=room, content=message, nonce=nonce)
