from django.db import models
from django.contrib.auth.models import User

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

class PreConstruction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='pre_construction')
    site_analysis = models.TextField()
    feasibility_study = models.FileField(upload_to='feasibility_studies/')
    budget_estimate = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Planning and Design
    architectural_plans = models.FileField(upload_to='architectural_plans/')
    engineering_plans = models.FileField(upload_to='engineering_plans/')
    
    # Permits and Approvals
    zoning_approval = models.BooleanField(default=False)
    building_permit = models.CharField(max_length=100, blank=True)
    environmental_clearance = models.BooleanField(default=False)

    # Contractor Selection
    contractor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracted_projects')
    contract_signed_date = models.DateField(null=True, blank=True)

class Construction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='construction')
    
    # Site Preparation
    site_cleared = models.BooleanField(default=False)
    foundation_laid = models.BooleanField(default=False)
    
    # Construction Progress
    structure_completion = models.IntegerField(default=0)  # Percentage
    electrical_work_completion = models.IntegerField(default=0)  # Percentage
    plumbing_completion = models.IntegerField(default=0)  # Percentage
    interior_completion = models.IntegerField(default=0)  # Percentage
    
    # Quality Control
    last_inspection_date = models.DateField(null=True, blank=True)
    inspection_status = models.CharField(max_length=20, choices=[
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ])

    # Safety
    safety_incidents = models.IntegerField(default=0)
    safety_meetings = models.IntegerField(default=0)

class PostConstruction(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='post_construction')
    
    # Final Inspections
    final_inspection_date = models.DateField(null=True, blank=True)
    final_inspection_passed = models.BooleanField(default=False)
    
    # Documentation
    as_built_drawings = models.FileField(upload_to='as_built_drawings/')
    operation_manuals = models.FileField(upload_to='operation_manuals/')
    warranties = models.FileField(upload_to='warranties/')
    
    # Handover
    client_walkthrough_date = models.DateField(null=True, blank=True)
    handover_date = models.DateField(null=True, blank=True)
    
    # Post-Occupancy
    defects_liability_period_end = models.DateField()
    
    # Feedback and Evaluation
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

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='project_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
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

class ChangeOrder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='change_orders')
    description = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_changes')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_changes')
    cost_impact = models.DecimalField(max_digits=12, decimal_places=2)
    time_impact = models.IntegerField()  # In days
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

# New models for Material, Equipment, and Labor Management

class Material(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ])

class Labor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    skills = models.TextField()
    certifications = models.TextField(blank=True)

class MaterialUsage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='material_usages')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    usage_date = models.DateField()

class EquipmentAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='equipment_assignments')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    assigned_from = models.DateField()
    assigned_to = models.DateField(null=True, blank=True)

class LaborAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='labor_assignments')
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
    assigned_from = models.DateField()
    assigned_to = models.DateField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2, default=0)

class Inventory(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='inventory')
    last_updated = models.DateTimeField(auto_now=True)

    def track_inventory(self):
        # Implement inventory tracking logic
        pass

class Procurement(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='procurement')
    last_order_date = models.DateTimeField(null=True, blank=True)

    def automate_procurement(self):
        # Implement procurement automation logic
        pass

class Budget(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='budget')
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def update_budget(self, amount):
        # Implement budget update logic
        pass

class Timeline(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='timeline')
    last_updated = models.DateTimeField(auto_now=True)

    def update_timeline(self, new_end_date):
        # Implement timeline update logic
        pass

class QualityControl(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='quality_control')

    def perform_inspection(self):
        # Implement quality inspection logic
        pass

    def perform_compliance_check(self):
        # Implement compliance check logic
        pass