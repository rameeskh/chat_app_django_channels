# yourapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import MentionNotificationLog  # Import your model
from .consumers import ChatConsumer, MentionNotificationHandler
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer




@receiver(post_save, sender=MentionNotificationLog)
def your_model_post_save(sender, instance, created, **kwargs):
    if created:
        # Your custom logic when a new instance is created
        print(f'A new instance of {sender.__name__} is created with ID {instance.id}')
        # room_name = "chat_" + instance.mentioned_user
        room_name = 'chat_lobby'
        chat_consumer = ChatConsumer()
        # channel_layer = async_to_sync(chat_consumer.channel_layer)
        channel_layer = get_channel_layer()

        # Send message to WebSocket group
        async_to_sync(channel_layer.group_send)(
            room_name,
            {
                "type": "chat.message",
                "message": f"One new log is created: {instance.comment}",
            },
        )
        # MentionNotificationHandler.send_notification(instance)
        print('below the mention notification called')

