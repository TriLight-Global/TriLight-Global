#Generic models for other apps

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    ROLES = (
        ('VISITOR', 'Visitor'),
        ('REGISTERED', 'Registered User'),
        ('AGENT', 'Agent'),
        ('OWNER', 'Property Owner'),
        ('DEVELOPER', 'Developer'),
        ('ADMIN', 'Admin')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='VISITOR')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class Property(models.Model):
    TYPES = (
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('CONDO', 'Condo'),
        ('LAND', 'Land'),
    )
    STATUS = (
        ('AVAILABLE', 'Available'),
        ('UNDER_DEVELOPMENT', 'Under Development'),
        ('SOLD', 'Sold'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default='AVAILABLE')
    address = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    features = ArrayField(models.CharField(max_length=100), blank=True)
    virtual_tour_url = models.URLField(blank=True)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_params = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)

class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20)

class MaintenanceRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Document(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='property_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    name = models.CharField(max_length=255)
    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20)
    due_date = models.DateField()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Viewing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='agent_viewings')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20)


