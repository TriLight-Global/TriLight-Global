# from django.db import models

# # Create your models here.
# class Document(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     file = models.FileField(upload_to='property_documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

# Documentation App

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    document_type = models.CharField(max_length=50, choices=[
        ('policy', 'Policy'),
        ('procedure', 'Procedure'),
        ('form', 'Form'),
        ('contract', 'Contract'),
        ('report', 'Report'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.TextField()

class DocumentApproval(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])
    comments = models.TextField(blank=True)

class DocumentAccess(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='access_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=[
        ('view', 'View'),
        ('edit', 'Edit'),
        ('download', 'Download'),
    ])

