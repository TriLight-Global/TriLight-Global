# Legal App

class Contract(models.Model):
    title = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=50, choices=[
        ('lease', 'Lease Agreement'),
        ('purchase', 'Purchase Agreement'),
        ('service', 'Service Contract'),
        ('employment', 'Employment Contract'),
    ])
    parties_involved = models.ManyToManyField(User, related_name='contracts')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
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

class LegalCase(models.Model):
    title = models.CharField(max_length=200)
    case_number = models.CharField(max_length=50, unique=True)
    case_type = models.CharField(max_length=50, choices=[
        ('eviction', 'Eviction'),
        ('property_damage', 'Property Damage'),
        ('contract_dispute', 'Contract Dispute'),
        ('personal_injury', 'Personal Injury'),
    ])
    plaintiff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plaintiff_cases')
    defendant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='defendant_cases')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='legal_cases')
    filing_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
        ('appealed', 'Appealed'),
    ])
    description = models.TextField()
    assigned_attorney = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_cases')

class LegalDocument(models.Model):
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=[
        ('complaint', 'Complaint'),
        ('motion', 'Motion'),
        ('evidence', 'Evidence'),
        ('settlement', 'Settlement Agreement'),
    ])
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='legal_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

class Compliance(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='compliance_records')
    compliance_type = models.CharField(max_length=50, choices=[
        ('zoning', 'Zoning'),
        ('building_code', 'Building Code'),
        ('fire_safety', 'Fire Safety'),
        ('accessibility', 'Accessibility'),
        ('environmental', 'Environmental'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
    ])
    last_inspection_date = models.DateField()
    next_inspection_date = models.DateField()
    notes = models.TextField(blank=True)

class LegalExpense(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=50, choices=[
        ('court_fees', 'Court Fees'),
        ('attorney_fees', 'Attorney Fees'),
        ('settlement', 'Settlement'),
        ('expert_witness', 'Expert Witness'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

class LegalCalendar(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='calendar_events')
    event_type = models.CharField(max_length=50, choices=[
        ('hearing', 'Hearing'),
        ('deposition', 'Deposition'),
        ('mediation', 'Mediation'),
        ('trial', 'Trial'),
    ])
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)


