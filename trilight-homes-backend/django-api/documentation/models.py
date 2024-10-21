# Documentation
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    document_type = models.CharField(max_length=50, choices=[
        ('policy', 'Policy'),
        ('procedure', 'Procedure'),
        ('form', 'Form'),
        ('contract', 'Contract'),
        ('report', 'Report'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentComment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DocumentTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class DocumentTagAssignment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(DocumentTag, on_delete=models.CASCADE)

class DocumentAttachment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='document_attachments/')
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    content_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DocumentShareLink(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='share_links')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    access_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=100, unique=True)

class DocumentWorkflow(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentWorkflowStep(models.Model):
    workflow = models.ForeignKey(DocumentWorkflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    approver_role = models.CharField(max_length=50)  # This could be linked to a Role model if you have one

class DocumentWorkflowInstance(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='workflow_instances')
    workflow = models.ForeignKey(DocumentWorkflow, on_delete=models.CASCADE)
    current_step = models.ForeignKey(DocumentWorkflowStep, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])

class DocumentRelationship(models.Model):
    from_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='related_from')
    to_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='related_to')
    relationship_type = models.CharField(max_length=50, choices=[
        ('supersedes', 'Supersedes'),
        ('references', 'References'),
        ('complements', 'Complements'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
