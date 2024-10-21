# Inspection
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Inspection(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='inspections')
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
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='inspection_schedules')
    frequency = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ])
    last_inspection_date = models.DateField(null=True, blank=True)
    next_inspection_date = models.DateField()

class InspectionTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    inspection_type = models.CharField(max_length=50, choices=[
        ('routine', 'Routine'),
        ('move_in', 'Move-in'),
        ('move_out', 'Move-out'),
        ('safety', 'Safety'),
    ])

class InspectionTemplateItem(models.Model):
    template = models.ForeignKey(InspectionTemplate, on_delete=models.CASCADE, related_name='items')
    area = models.CharField(max_length=100)
    item = models.CharField(max_length=100)

class InspectionReport(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE, related_name='report')
    summary = models.TextField()
    recommendations = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='inspection_reports/', null=True, blank=True)

class InspectionNotification(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inspection_notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

class InspectionAttachment(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='inspection_attachments/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class InspectionFollowUp(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='follow_ups')
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_follow_ups')

class InspectionComment(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class InspectionChecklistItem(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='checklist_items')
    item = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

class InspectionSignOff(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE, related_name='sign_off')
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='signed_inspections')
    signature = models.ImageField(upload_to='inspection_signatures/')
    signed_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)


