from django.db import models

# Create your models here.
# Inspections App

class Inspection(models.Model):
    property = models.ForeignKey('property_listing.Property', on_delete=models.CASCADE, related_name='inspections')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_inspections')
    inspection_date = models.DateTimeField()
    inspection_type = models.CharField(max_length=50, choices=[
        ('routine', 'Routine'),
        ('move_in', 'Move-in'),
        ('move_out', 'Move-out'),
        ('complaint', 'Complaint-based'),
        ('safety', 'Safety'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    overall_condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ])
    notes = models.TextField(blank=True)

class InspectionItem(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='items')
    area = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('n/a', 'Not Applicable'),
    ])
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='inspection_photos/', blank=True, null=True)

class MaintenanceRequest(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='maintenance_requests')
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ])
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_maintenance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InspectionSchedule(models.Model):
    property = models.ForeignKey('property_listing.Property', on_delete=models.CASCADE, related_name='inspection_schedules')
    frequency = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ])
    last_inspection_date = models.DateField(null=True, blank=True)
    next_inspection_date = models.DateField()

