# chat/consumers.py
import json

from django.contrib.auth.models import User


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print('group name', self.room_group_name, 'channel_name', self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": "The first message while connecting it"}
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class MentionNotificationHandler:
    @classmethod
    def send_notification(cls, instance):
        user = User.objects.get(id=instance.mentioned_user_id)
        room_name = "chat_" + user.username
        print('room name', room_name)
        # chat_consumer = ChatConsumer()

        # channel_layer = chat_consumer.get_channel_layer()
        # channel_layer.group_add('chat_lobby', 'specific.53e5edf6f7584214b34287c87744bed5!7fc25b4078e14e50bda8c925f253b2e1')

        # # Send message to WebSocket group
        # async_to_sync(channel_layer.group_send)(
        #     room_name,
        #     {
        #         "type": "chat.message",
        #         "message": f"One new log is created: {instance.comment}",
        #     },
        # )
    print('send notification function is called')
