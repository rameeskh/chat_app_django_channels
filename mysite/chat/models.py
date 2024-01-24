from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class MentionNotificationLog(models.Model):
    notification_id = models.CharField(max_length=255, unique=True)
    comment = models.CharField(max_length=20)
    mentioned_user = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    class Meta:
        db_table = 'mention_notification_log'
    
    def send_notification(self):
        channel_layer = get_channel_layer()
        room_group_name = f"chat_{self.mentioned_user}"

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                "type": "chat.message",
                "message": {
                    "notification_id": self.notification_id,
                    "comment": self.comment,
                    "mentioned_user": self.mentioned_user,
                    "created_at": self.created_at.isoformat(),
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                    "is_read": self.is_read,
                    "is_edited": self.is_edited,
                },
            },
        )
    print("send notificaiton fucntion is called")


@receiver(post_save, sender=MentionNotificationLog)
def send_notification_on_creation(sender, instance, created, **kwargs):
    if created:
        instance.send_notification()