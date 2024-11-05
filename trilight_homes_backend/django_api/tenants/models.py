# Tenants

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    employment_status = models.CharField(max_length=50, choices=[
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
        ('student', 'Student'),
    ])
    employer_name = models.CharField(max_length=100, blank=True)
    employer_phone = models.CharField(max_length=20, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    credit_score = models.PositiveIntegerField(null=True, blank=True)
    previous_address = models.TextField(blank=True)
    has_pets = models.BooleanField(default=False)
    pet_details = models.TextField(blank=True)

class Lease(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    lease_type = models.CharField(max_length=50, choices=[
        ('fixed_term', 'Fixed Term'),
        ('month_to_month', 'Month-to-Month'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ])
    document = models.FileField(upload_to='lease_documents/')
    special_terms = models.TextField(blank=True)
    is_cosigned = models.BooleanField(default=False)

class RentPayment(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='rent_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('online_payment', 'Online Payment'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('late', 'Late'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ])
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='maintenance_requests')
    request_type = models.CharField(max_length=50, choices=[
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('hvac', 'HVAC'),
        ('appliance', 'Appliance'),
        ('structural', 'Structural'),
        ('pest_control', 'Pest Control'),
        ('other', 'Other'),
    ])
    description = models.TextField()
    urgency = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_maintenance_requests')

class TenantDocument(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=[
        ('id', 'Identification'),
        ('income_proof', 'Proof of Income'),
        ('reference', 'Reference Letter'),
        ('background_check', 'Background Check'),
        ('employment_verification', 'Employment Verification'),
        ('rental_history', 'Rental History'),
    ])
    file = models.FileField(upload_to='tenant_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_tenant_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class TenantReview(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_reviews_given')
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='tenant_reviews')
    is_anonymous = models.BooleanField(default=False)

class TenantCommunication(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='communications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_tenant_communications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    communication_type = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-App Message'),
    ])
    subject = models.CharField(max_length=255, blank=True)
    attachment = models.FileField(upload_to='tenant_communication_attachments/', null=True, blank=True)

class TenantPreference(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='preferences')
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS'),
    ])
    newsletter_subscription = models.BooleanField(default=True)
    maintenance_notification = models.BooleanField(default=True)
    rent_reminder = models.BooleanField(default=True)
    language_preference = models.CharField(max_length=10, default='en')

class TenantReferral(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='referrals')
    referred_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='referred_by')
    referral_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])
    reward_given = models.BooleanField(default=False)
    reward_details = models.TextField(blank=True)

class TenantNotification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=[
        ('rent_due', 'Rent Due'),
        ('maintenance_update', 'Maintenance Update'),
        ('lease_expiry', 'Lease Expiry'),
        ('general', 'General Notification'),
    ])

class TenantBilling(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='billings')
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='billings')
    bill_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class TenantUtilityUsage(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='utility_usages')
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='utility_usages')
    utility_type = models.CharField(max_length=50, choices=[
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
    ])
    usage_date = models.DateField()
    usage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class TenantInsurance(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='insurances')
    insurance_provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    document = models.FileField(upload_to='tenant_insurance_documents/', null=True, blank=True)

class TenantVehicle(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=20)
    parking_spot = models.CharField(max_length=20, blank=True)

class TenantPet(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='pets')
    pet_type = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_service_animal = models.BooleanField(default=False)
    documentation = models.FileField(upload_to='tenant_pet_documents/', null=True, blank=True)

class TenantEmergencyContact(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

class TenantReference(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    reference_letter = models.FileField(upload_to='tenant_reference_letters/', null=True, blank=True)
    verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)

class TenantWorkOrder(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='work_orders')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='tenant_work_orders')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_work_orders')
    notes = models.TextField(blank=True)

class TenantLedger(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='ledger_entries')
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='ledger_entries')
    date = models.DateField()
    description = models.CharField(max_length=255)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
