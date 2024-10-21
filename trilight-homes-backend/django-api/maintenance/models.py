from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')

class MaintenanceRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency')
    ])
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MaintenanceTask(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    description = models.TextField()
    estimated_time = models.DurationField()
    actual_time = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])

class ScheduledMaintenance(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='scheduled_maintenance')
    title = models.CharField(max_length=200)
    description = models.TextField()
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ])
    last_performed = models.DateField(null=True, blank=True)
    next_due = models.DateField()

class MaintenanceLog(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_logs')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    date_performed = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Inventory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    reorder_level = models.IntegerField()

class InventoryUsage(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='usages')
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='inventory_usages')
    quantity_used = models.IntegerField()
    date_used = models.DateField()

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    services = models.TextField()

class VendorAssignment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assignments')
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='vendor_assignments')
    assigned_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)