# Land

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from .VerificationSteps import VerificationStep

User = get_user_model()

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

    title = models.CharField(max_length=200)
    description = models.TextField()
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lands')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='land_documents/')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

class CommunityVerification(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='community_verifications')
    verifier_name = models.CharField(max_length=100)
    verifier_title = models.CharField(max_length=100)
    verification_date = models.DateField()
    is_verified = models.BooleanField()
    notes = models.TextField()

class LandDispute(models.Model):
    DISPUTE_TYPES = [
        ('BOUNDARY', 'Boundary Dispute'),
        ('OWNERSHIP', 'Ownership Dispute'),
        ('INHERITANCE', 'Inheritance Dispute'),
        ('ENCROACHMENT', 'Encroachment'),
        ('TITLE', 'Title Dispute'),
        ('OTHER', 'Other'),
    ]

    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='disputes')
    dispute_type = models.CharField(max_length=20, choices=DISPUTE_TYPES)
    description = models.TextField()
    start_date = models.DateField()
    resolution_date = models.DateField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    resolution_details = models.TextField(blank=True)

class LandVerification(models.Model):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    land_parcel = models.OneToOneField(LandParcel, on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='PENDING')
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

class VerificationCheckpoint(models.Model):
    verification = models.ForeignKey(LandVerification, on_delete=models.CASCADE, related_name='checkpoints')
    step = models.ForeignKey(VerificationStep, on_delete=models.CASCADE)  # Use the imported VerificationStep model
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    result = models.TextField(blank=True)
    attachments = models.FileField(upload_to='verification_attachments/', null=True, blank=True)

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

class LandReview(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class LandAmenity(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    description = models.TextField()

class LandImage(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='land_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class LandDevelopmentPlan(models.Model):
    land_parcel = models.OneToOneField(LandParcel, on_delete=models.CASCADE, related_name='development_plan')
    plan_description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_duration = models.DurationField()
    approved = models.BooleanField(default=False)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)

class LandValuation(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='valuations')
    valuation_date = models.DateField()
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
    valuer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    valuation_method = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

class LandTax(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='taxes')
    tax_year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    receipt_number = models.CharField(max_length=100, blank=True)

class LandSurvey(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='surveys')
    survey_date = models.DateField()
    surveyor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    survey_report = models.FileField(upload_to='land_surveys/')
    notes = models.TextField(blank=True)

class LandOwnershipHistory(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='ownership_history')
    previous_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='previously_owned_lands')
    new_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newly_owned_lands')
    transfer_date = models.DateField()
    transfer_reason = models.CharField(max_length=100)
    transfer_document = models.FileField(upload_to='land_transfer_documents/', null=True, blank=True)

class LandUsePermit(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='use_permits')
    permit_type = models.CharField(max_length=100)
    issued_by = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    permit_document = models.FileField(upload_to='land_use_permits/')
    is_active = models.BooleanField(default=True)
