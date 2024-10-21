from django.db import models
from django.contrib.auth.models import User

class PropertyIndex(models.Model):
    property = models.OneToOneField('properties.Property', on_delete=models.CASCADE, related_name='index')
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    amenities = models.JSONField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    preferred_locations = models.JSONField()
    preferred_property_types = models.JSONField()
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    min_bathrooms = models.PositiveIntegerField(null=True, blank=True)
    preferred_amenities = models.JSONField()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.TextField()
    filters = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

class PropertyView(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)