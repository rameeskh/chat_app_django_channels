from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User



class MentionNotificationLog(models.Model):
    notification_id = models.CharField(max_length=255, unique=True)
    comment = models.CharField(max_length=20)
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    class Meta:
        db_table = 'mention_notification_log'

