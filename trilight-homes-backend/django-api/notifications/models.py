from django.db import models

# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)
#     read_at = models.DateTimeField(null=True, blank=True)

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

# class MaintenanceRequest(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     description = models.TextField()
#     status = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
