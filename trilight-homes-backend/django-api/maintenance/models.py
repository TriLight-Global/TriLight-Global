# Maintenance
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MaintenanceRequest(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='maintenance_requests')
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
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='scheduled_maintenance')
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
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='maintenance_logs')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    date_performed = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class MaintenanceInventory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    reorder_level = models.IntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

class InventoryUsage(models.Model):
    inventory = models.ForeignKey(MaintenanceInventory, on_delete=models.CASCADE, related_name='usages')
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='inventory_usages')
    quantity_used = models.IntegerField()
    date_used = models.DateField()

class MaintenanceVendor(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    services = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

class VendorAssignment(models.Model):
    vendor = models.ForeignKey(MaintenanceVendor, on_delete=models.CASCADE, related_name='assignments')
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='vendor_assignments')
    assigned_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class MaintenanceSkill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class MaintenanceWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(MaintenanceSkill)
    availability = models.CharField(max_length=20, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('on_call', 'On Call')
    ])

class MaintenanceEquipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_due = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('under_maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service')
    ])

class MaintenanceCost(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='costs')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()
    paid = models.BooleanField(default=False)

class MaintenanceReport(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='maintenance_reports')
    start_date = models.DateField()
    end_date = models.DateField()
    total_requests = models.IntegerField()
    completed_requests = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

class MaintenanceNotification(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

class MaintenanceAttachment(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='maintenance_attachments/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
