import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_superuser:
            self.room_group_name = 'admin_chat'
        else:
            self.room_group_name = f'chat_{self.user.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        if 'receiver_id' in text_data_json:
            receiver_id = text_data_json['receiver_id']
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
        else:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(is_superuser=True).first()

        chat = Chat.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

        if sender.is_superuser:
            room_group_name = f'chat_{receiver.id}'
        else:
            room_group_names = ['admin_chat', f'chat_{sender.id}']

        message_data = {
            'type': 'chat_message',
            'message': message,
            'sender': sender.username,
            'sender_id': sender.id,
            'receiver': receiver.username,
            'receiver_id': receiver.id,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

        if isinstance(room_group_names, list):
            for group_name in room_group_names:
                await self.channel_layer.group_send(
                    group_name,
                    message_data
                )
        else:
            await self.channel_layer.group_send(
                room_group_name,
                message_data
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))