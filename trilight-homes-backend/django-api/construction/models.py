# Construction

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold')
    ])
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='construction_projects')
    budget = models.DecimalField(max_digits=12, decimal_places=2)

class PreConstruction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='pre_construction')
    site_analysis = models.TextField()
    feasibility_study = models.FileField(upload_to='feasibility_studies/')
    budget_estimate = models.DecimalField(max_digits=12, decimal_places=2)
    architectural_plans = models.FileField(upload_to='architectural_plans/')
    engineering_plans = models.FileField(upload_to='engineering_plans/')
    zoning_approval = models.BooleanField(default=False)
    building_permit = models.CharField(max_length=100, blank=True)
    environmental_clearance = models.BooleanField(default=False)
    contractor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracted_projects')
    contract_signed_date = models.DateField(null=True, blank=True)

class Construction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='construction')
    site_cleared = models.BooleanField(default=False)
    foundation_laid = models.BooleanField(default=False)
    structure_completion = models.IntegerField(default=0)  # Percentage
    electrical_work_completion = models.IntegerField(default=0)  # Percentage
    plumbing_completion = models.IntegerField(default=0)  # Percentage
    interior_completion = models.IntegerField(default=0)  # Percentage
    last_inspection_date = models.DateField(null=True, blank=True)
    inspection_status = models.CharField(max_length=20, choices=[
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ])
    safety_incidents = models.IntegerField(default=0)
    safety_meetings = models.IntegerField(default=0)

class PostConstruction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='post_construction')
    final_inspection_date = models.DateField(null=True, blank=True)
    final_inspection_passed = models.BooleanField(default=False)
    as_built_drawings = models.FileField(upload_to='as_built_drawings/')
    operation_manuals = models.FileField(upload_to='operation_manuals/')
    warranties = models.FileField(upload_to='warranties/')
    client_walkthrough_date = models.DateField(null=True, blank=True)
    handover_date = models.DateField(null=True, blank=True)
    defects_liability_period_end = models.DateField()
    client_satisfaction_score = models.IntegerField(null=True, blank=True)  # Scale of 1-10
    project_evaluation_report = models.TextField(blank=True)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue')
    ])
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])

class ConstructionDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='project_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    document_type = models.CharField(max_length=50, choices=[
        ('contract', 'Contract'),
        ('permit', 'Permit'),
        ('inspection_report', 'Inspection Report'),
        ('change_order', 'Change Order'),
        ('other', 'Other')
    ])

class ConstructionIssue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues')
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ])
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolution = models.TextField(blank=True)

class ChangeOrder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='change_orders')
    description = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_changes')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_changes')
    cost_impact = models.DecimalField(max_digits=12, decimal_places=2)
    time_impact = models.IntegerField(help_text="Impact in days")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

class ConstructionMaterial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, related_name='supplied_materials')

class ConstructionEquipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ])

class ConstructionWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    skills = models.TextField()
    certifications = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)

class MaterialUsage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='material_usages')
    material = models.ForeignKey(ConstructionMaterial, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    usage_date = models.DateField()
    used_by = models.ForeignKey(ConstructionWorker, on_delete=models.SET_NULL, null=True)

class EquipmentAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='equipment_assignments')
    equipment = models.ForeignKey(ConstructionEquipment, on_delete=models.CASCADE)
    assigned_from = models.DateField()
    assigned_to = models.DateField(null=True, blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class WorkerAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='worker_assignments')
    worker = models.ForeignKey(ConstructionWorker, on_delete=models.CASCADE)
    assigned_from = models.DateField()
    assigned_to = models.DateField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    role = models.CharField(max_length=100)

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    products_services = models.TextField()

class ConstructionPhase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed')
    ])
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class QualityControl(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='quality_controls')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    inspection_date = models.DateField()
    area_inspected = models.CharField(max_length=100)
    passed = models.BooleanField()
    notes = models.TextField()
    followup_required = models.BooleanField(default=False)
    followup_date = models.DateField(null=True, blank=True)

class ConstructionBudget(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='budget')
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    spent_to_date = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def remaining_budget(self):
        return self.total_budget - self.spent_to_date

class ConstructionTimeline(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='timeline')
    original_end_date = models.DateField()
    current_end_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    def is_delayed(self):
        return self.current_end_date > self.original_end_date

class ConstructionMeeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='meetings')
    meeting_date = models.DateTimeField()
    meeting_type = models.CharField(max_length=50, choices=[
        ('kickoff', 'Kickoff'),
        ('progress', 'Progress'),
        ('stakeholder', 'Stakeholder'),
        ('safety', 'Safety'),
    ])
    attendees = models.ManyToManyField(User, related_name='attended_meetings')
    minutes = models.TextField()
    action_items = models.TextField()

class ConstructionSafetyReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='safety_reports')
    report_date = models.DateField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    incident_description = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    followup_required = models.BooleanField(default=False)
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])