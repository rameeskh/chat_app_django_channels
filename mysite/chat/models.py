from django.db import models


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