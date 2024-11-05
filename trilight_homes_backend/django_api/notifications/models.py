from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('system', 'System Notification'),
        ('maintenance', 'Maintenance Update'),
        ('legal', 'Legal Update'),
        ('payment', 'Payment Reminder'),
        ('lease', 'Lease Update'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

class NotificationAction(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='actions')
    label = models.CharField(max_length=100)
    url = models.URLField()

class PushNotificationDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_notification_devices')
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=50)
    push_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)

class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    max_notifications_per_day = models.PositiveIntegerField(default=50)