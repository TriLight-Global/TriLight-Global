from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class ExternalLandListing(models.Model):
    LISTING_PLATFORMS = [
        ('JIJI', 'Jiji'),
        ('OLIST', 'OList'),
        ('PRIVATEPROPERTY', 'Private Property'),
        ('PROPERTYPRO', 'Property Pro'),
        ('OTHER', 'Other'),
    ]

    platform = models.CharField(max_length=20, choices=LISTING_PLATFORMS)
    external_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    listing_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.platform} - {self.title}"

class LandOwnershipType(models.Model):
    OWNERSHIP_TYPES = [
        ('ESTATE', 'Estate Land'),
        ('PERSONAL', 'Personal Land'),
        ('COMMUNITY', 'Community Land'),
        ('GOVERNMENT', 'Government Land'),
        ('CORPORATE', 'Corporate Land'),
    ]

    type = models.CharField(max_length=20, choices=OWNERSHIP_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.get_type_display()

class LandDocument(models.Model):
    DOCUMENT_TYPES = [
        ('C_OF_O', 'Certificate of Occupancy'),
        ('GOVERNORS_CONSENT', "Governor's Consent"),
        ('DEED_OF_ASSIGNMENT', 'Deed of Assignment'),
        ('SURVEY_PLAN', 'Survey Plan'),
        ('LAND_AGREEMENT', 'Land Agreement'),
        ('RECEIPT', 'Payment Receipt'),
        ('OTHER', 'Other'),
    ]

    land_parcel = models.ForeignKey('LandParcel', on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='land_documents/')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.land_parcel.title} - {self.get_document_type_display()}"

class CommunityVerification(models.Model):
    land_parcel = models.ForeignKey('LandParcel', on_delete=models.CASCADE, related_name='community_verifications')
    verifier_name = models.CharField(max_length=100)
    verifier_title = models.CharField(max_length=100)
    verification_date = models.DateField()
    is_verified = models.BooleanField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.land_parcel.title} - {self.verifier_name}"

class LandDispute(models.Model):
    DISPUTE_TYPES = [
        ('BOUNDARY', 'Boundary Dispute'),
        ('OWNERSHIP', 'Ownership Dispute'),
        ('INHERITANCE', 'Inheritance Dispute'),
        ('ENCROACHMENT', 'Encroachment'),
        ('TITLE', 'Title Dispute'),
        ('OTHER', 'Other'),
    ]

    land_parcel = models.ForeignKey('LandParcel', on_delete=models.CASCADE, related_name='disputes')
    dispute_type = models.CharField(max_length=20, choices=DISPUTE_TYPES)
    description = models.TextField()
    start_date = models.DateField()
    resolution_date = models.DateField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    resolution_details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.land_parcel.title} - {self.get_dispute_type_display()}"

class VerificationStep(MPTTModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class LandVerification(models.Model):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    land_parcel = models.OneToOneField('LandParcel', on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='PENDING')
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.land_parcel.title} - {self.status}"

class VerificationCheckpoint(models.Model):
    verification = models.ForeignKey(LandVerification, on_delete=models.CASCADE, related_name='checkpoints')
    step = models.ForeignKey(VerificationStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    result = models.TextField(blank=True)
    attachments = models.FileField(upload_to='verification_attachments/', null=True, blank=True)

    def __str__(self):
        return f"{self.verification.land_parcel.title} - {self.step.name}"

class LandParcel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    ownership_type = models.ForeignKey(LandOwnershipType, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lands')
    is_verified = models.BooleanField(default=False)
    listed_externally = models.ForeignKey(ExternalLandListing, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class LandParcel(models.Model):
    LAND_TYPES = [
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('AGRICULTURAL', 'Agricultural'),
        ('INDUSTRIAL', 'Industrial'),
    ]

    ZONING_TYPES = [
        ('R1', 'Single Family Residential'),
        ('R2', 'Multi-Family Residential'),
        ('C1', 'Commercial'),
        ('I1', 'Light Industrial'),
        ('A1', 'Agricultural'),
    ]

    parcel_id = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)  # in square meters
    land_type = models.CharField(max_length=20, choices=LAND_TYPES)
    zoning = models.CharField(max_length=20, choices=ZONING_TYPES)
    topography = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parcel_id} - {self.address}"

class LandOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    id_number = models.CharField(max_length=50, unique=True)
    parcels = models.ManyToManyField(LandParcel, related_name='owners')

    def __str__(self):
        return self.user.get_full_name()

class LandDocument(models.Model):
    DOCUMENT_TYPES = [
        ('DEED', 'Property Deed'),
        ('SURVEY', 'Land Survey'),
        ('TAX', 'Tax Certificate'),
        ('TITLE', 'Title Insurance'),
        ('ZONING', 'Zoning Permit'),
        ('ENVIRONMENTAL', 'Environmental Assessment'),
    ]

    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='land_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.land_parcel.parcel_id} - {self.get_document_type_display()}"

class LandSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.TextField()
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    land_type = models.CharField(max_length=20, choices=LandParcel.LAND_TYPES, null=True, blank=True)
    zoning = models.CharField(max_length=20, choices=LandParcel.ZONING_TYPES, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.search_date}"

class LandVerification(models.Model):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    land_parcel = models.OneToOneField(LandParcel, on_delete=models.CASCADE, related_name='verification')
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='PENDING')
    start_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.land_parcel.parcel_id} - {self.status}"

class VerificationStep(models.Model):
    verification = models.ForeignKey(LandVerification, on_delete=models.CASCADE, related_name='steps')
    step_name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.verification.land_parcel.parcel_id} - {self.step_name}"

class LandPurchase(models.Model):
    PURCHASE_STATUS = [
        ('INITIATED', 'Initiated'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PURCHASE_STATUS, default='INITIATED')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    initiation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    agreement_document = models.FileField(upload_to='purchase_agreements/', null=True, blank=True)

    def __str__(self):
        return f"{self.land_parcel.parcel_id} - {self.buyer.username} - {self.status}"

class LandReview(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.land_parcel.parcel_id} - {self.reviewer.username} - {self.rating}"

class LandAmenity(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.land_parcel.parcel_id} - {self.name}"

class EmergencyResponse(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='emergency_responses')
    incident_type = models.CharField(max_length=100)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('RESOLVED', 'Resolved')])

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)  # e.g., 'EMERGENCY', 'MAINTENANCE', 'DOCUMENT'

class PropertyMaintenance(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='maintenance_records')
    description = models.TextField()
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')])

class LeaseAgreement(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='lease_agreements')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    agreement_document = models.FileField(upload_to='lease_agreements/')

class PermitDocument(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='permits')
    document_type = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    document_file = models.FileField(upload_to='permit_documents/')
    status = models.CharField(max_length=20, choices=[('VALID', 'Valid'), ('EXPIRED', 'Expired'), ('PENDING', 'Pending Renewal')])

class QualityControl(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='quality_checks')
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    compliance_status = models.BooleanField()
    notes = models.TextField()

class RegulatoryApproval(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='regulatory_approvals')
    approval_type = models.CharField(max_length=100)
    issuing_authority = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('EXPIRED', 'Expired'), ('PENDING', 'Pending Renewal')])

class TenantMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    services = models.TextField()

class TransactionTimeline(models.Model):
    land_purchase = models.ForeignKey(LandPurchase, on_delete=models.CASCADE, related_name='timeline_events')
    event_description = models.TextField()
    event_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('DELAYED', 'Delayed')])

class SharedDocument(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    shared_with = models.ManyToManyField(User, related_name='shared_documents')
    document = models.FileField(upload_to='shared_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()