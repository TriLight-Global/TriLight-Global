# Legal

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Contract(models.Model):
    title = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=50, choices=[
        ('lease', 'Lease Agreement'),
        ('purchase', 'Purchase Agreement'),
        ('service', 'Service Contract'),
        ('employment', 'Employment Contract'),
    ])
    parties_involved = models.ManyToManyField(User, related_name='contracts')
    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ])
    document = models.FileField(upload_to='contracts/')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_contracts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LegalCase(models.Model):
    title = models.CharField(max_length=200)
    case_number = models.CharField(max_length=50, unique=True)
    case_type = models.CharField(max_length=50, choices=[
        ('eviction', 'Eviction'),
        ('property_damage', 'Property Damage'),
        ('contract_dispute', 'Contract Dispute'),
        ('personal_injury', 'Personal Injury'),
        ('landlord_tenant', 'Landlord-Tenant Dispute'),
        ('property_rights', 'Property Rights'),
        ('zoning', 'Zoning Issue'),
    ])
    plaintiff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plaintiff_cases')
    defendant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='defendant_cases')
    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='legal_cases')
    filing_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
        ('appealed', 'Appealed'),
        ('settled', 'Settled'),
    ])
    description = models.TextField()
    assigned_attorney = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_cases')
    court = models.CharField(max_length=100, blank=True)
    judge = models.CharField(max_length=100, blank=True)
    next_hearing_date = models.DateTimeField(null=True, blank=True)

class LegalDocument(models.Model):
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=[
        ('complaint', 'Complaint'),
        ('motion', 'Motion'),
        ('evidence', 'Evidence'),
        ('settlement', 'Settlement Agreement'),
        ('court_order', 'Court Order'),
        ('affidavit', 'Affidavit'),
        ('subpoena', 'Subpoena'),
    ])
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='legal_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=False)

class Compliance(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='compliance_records')
    compliance_type = models.CharField(max_length=50, choices=[
        ('zoning', 'Zoning'),
        ('building_code', 'Building Code'),
        ('fire_safety', 'Fire Safety'),
        ('accessibility', 'Accessibility'),
        ('environmental', 'Environmental'),
        ('health_safety', 'Health and Safety'),
        ('licensing', 'Licensing and Permits'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('exempt', 'Exempt'),
    ])
    last_inspection_date = models.DateField()
    next_inspection_date = models.DateField()
    inspector = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    documents = models.ManyToManyField(LegalDocument, blank=True, related_name='compliance_records')

class LegalExpense(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=50, choices=[
        ('court_fees', 'Court Fees'),
        ('attorney_fees', 'Attorney Fees'),
        ('settlement', 'Settlement'),
        ('expert_witness', 'Expert Witness'),
        ('filing_fees', 'Filing Fees'),
        ('deposition_costs', 'Deposition Costs'),
        ('travel_expenses', 'Travel Expenses'),
        ('miscellaneous', 'Miscellaneous'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    receipt = models.FileField(upload_to='legal_expense_receipts/', null=True, blank=True)

class LegalCalendar(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='calendar_events')
    event_type = models.CharField(max_length=50, choices=[
        ('hearing', 'Hearing'),
        ('deposition', 'Deposition'),
        ('mediation', 'Mediation'),
        ('trial', 'Trial'),
        ('settlement_conference', 'Settlement Conference'),
        ('filing_deadline', 'Filing Deadline'),
        ('client_meeting', 'Client Meeting'),
    ])
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    attendees = models.ManyToManyField(User, related_name='legal_calendar_events')
    reminder_sent = models.BooleanField(default=False)

class LegalNotice(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='legal_notices')
    notice_type = models.CharField(max_length=50, choices=[
        ('eviction', 'Eviction Notice'),
        ('lease_violation', 'Lease Violation'),
        ('rent_increase', 'Rent Increase'),
        ('termination', 'Lease Termination'),
        ('entry', 'Notice of Entry'),
        ('repair', 'Notice to Repair'),
    ])
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_legal_notices')
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_legal_notices')
    send_date = models.DateField()
    effective_date = models.DateField()
    description = models.TextField()
    document = models.FileField(upload_to='legal_notices/')
    delivery_method = models.CharField(max_length=50, choices=[
        ('mail', 'Mail'),
        ('email', 'Email'),
        ('hand_delivered', 'Hand Delivered'),
        ('posted', 'Posted on Property'),
    ])
    proof_of_service = models.FileField(upload_to='proof_of_service/', null=True, blank=True)

class LegalConsultation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='legal_consultations')
    attorney = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_consultations')
    date_time = models.DateTimeField()
    duration = models.DurationField()
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)

class ContractTemplate(models.Model):
    name = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=50, choices=[
        ('lease', 'Lease Agreement'),
        ('purchase', 'Purchase Agreement'),
        ('service', 'Service Contract'),
        ('employment', 'Employment Contract'),
    ])
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class LegalDisclosure(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='legal_disclosures')
    disclosure_type = models.CharField(max_length=50, choices=[
        ('lead_paint', 'Lead-Based Paint'),
        ('asbestos', 'Asbestos'),
        ('mold', 'Mold'),
        ('flood_zone', 'Flood Zone'),
        ('pest_infestation', 'Pest Infestation'),
        ('structural_issues', 'Structural Issues'),
        ('natural_hazards', 'Natural Hazards'),
    ])
    description = models.TextField()
    date_disclosed = models.DateField()
    disclosed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='made_disclosures')
    acknowledged_by = models.ManyToManyField(User, related_name='acknowledged_disclosures')
    document = models.FileField(upload_to='legal_disclosures/', null=True, blank=True)

class LitigationHold(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='litigation_holds')
    hold_date = models.DateField()
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    custodians = models.ManyToManyField(User, related_name='litigation_holds')
    data_types = models.TextField(help_text="Types of data to be preserved")
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_litigation_holds')

class LegalResearch(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='legal_research')
    topic = models.CharField(max_length=200)
    researcher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_conducted = models.DateField()
    findings = models.TextField()
    sources = models.TextField()
    relevance = models.TextField(help_text="Relevance to the case")
    document = models.FileField(upload_to='legal_research/', null=True, blank=True)

class LegalTeam(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='legal_team')
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('lead_attorney', 'Lead Attorney'),
        ('associate_attorney', 'Associate Attorney'),
        ('paralegal', 'Paralegal'),
        ('legal_assistant', 'Legal Assistant'),
        ('expert_witness', 'Expert Witness'),
    ])
    assigned_date = models.DateField()
    removed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class LegalDeadline(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='legal_deadlines')
    description = models.CharField(max_length=200)
    deadline_date = models.DateTimeField()
    responsible_party = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('extended', 'Extended'),
    ])
    reminder_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
