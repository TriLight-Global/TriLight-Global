# Properties
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPES = [
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('CONDO', 'Condominium'),
        ('TOWNHOUSE', 'Townhouse'),
        ('COMMERCIAL', 'Commercial'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNDER_CONTRACT', 'Under Contract'),
        ('SOLD', 'Sold'),
        ('RENTED', 'Rented'),
        ('OFF_MARKET', 'Off Market'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    address = models.OneToOneField('Address', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    area = models.DecimalField(max_digits=10, decimal_places=2)  # in square feet/meters
    year_built = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField(default=0)
    features = ArrayField(models.CharField(max_length=100), blank=True)
    amenities = models.ManyToManyField('Amenity', related_name='properties')
    virtual_tour_url = models.URLField(blank=True)
    energy_rating = models.CharField(max_length=10, blank=True)
    listed_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # CSS class or icon name

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

class PropertyDocument(models.Model):
    DOCUMENT_TYPES = [
        ('DEED', 'Deed'),
        ('TAX_RECORD', 'Tax Record'),
        ('FLOOR_PLAN', 'Floor Plan'),
        ('INSPECTION_REPORT', 'Inspection Report'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='property_documents/')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

class PropertyHistory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='history')
    event_type = models.CharField(max_length=50)  # e.g., 'PRICE_CHANGE', 'STATUS_CHANGE'
class PropertyHistory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='history')
    event_type = models.CharField(max_length=50)  # e.g., 'PRICE_CHANGE', 'STATUS_CHANGE'
    event_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_features')
    feature = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class PropertyReview(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyView(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_views')
    viewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    view_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    added_date = models.DateTimeField(auto_now_add=True)

class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    inquirer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_inquiries')
    message = models.TextField()
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)

class PropertyValuation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='valuations')
    valuation_date = models.DateField()
    valuation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    valuer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    valuation_method = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

class PropertyTax(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='taxes')
    tax_year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)

class PropertyInsurance(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='insurances')
    insurance_provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class PropertyMortgage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='mortgages')
    lender = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_years = models.PositiveIntegerField()
    start_date = models.DateField()
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)

class OpenHouse(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='open_houses')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='hosted_open_houses')
    notes = models.TextField(blank=True)

class PropertyComparable(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comparables')
    comparable_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='compared_to')
    similarity_score = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)

class PropertyFloorPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='floor_plans')
    name = models.CharField(max_length=100)  # e.g., "First Floor", "Basement"
    image = models.ImageField(upload_to='property_floor_plans/')
    description = models.TextField(blank=True)

class PropertyAppliance(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='appliances')
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiration = models.DateField(null=True, blank=True)

class PropertySchoolDistrict(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='school_districts')
    district_name = models.CharField(max_length=100)
    elementary_school = models.CharField(max_length=100)
    middle_school = models.CharField(max_length=100)
    high_school = models.CharField(max_length=100)
    district_rating = models.PositiveIntegerField(null=True, blank=True)

class PropertyNearbyPlace(models.Model):
    PLACE_TYPES = [
        ('RESTAURANT', 'Restaurant'),
        ('SCHOOL', 'School'),
        ('HOSPITAL', 'Hospital'),
        ('SHOPPING', 'Shopping'),
        ('PARK', 'Park'),
        ('PUBLIC_TRANSPORT', 'Public Transport'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='nearby_places')
    name = models.CharField(max_length=100)
    place_type = models.CharField(max_length=20, choices=PLACE_TYPES)
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # in miles or kilometers
    travel_time = models.PositiveIntegerField(help_text="Travel time in minutes")

class PropertyListing(models.Model):
    LISTING_TYPES = [
        ('FOR_SALE', 'For Sale'),
        ('FOR_RENT', 'For Rent'),
        ('AUCTION', 'Auction'),
    ]

    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='listing')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    list_date = models.DateField()
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='agent_listings')
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    listing_description = models.TextField()
    showing_instructions = models.TextField(blank=True)

class PropertyRental(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='rental')
    is_furnished = models.BooleanField(default=False)
    minimum_lease_term = models.PositiveIntegerField(help_text="Minimum lease term in months")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    pet_policy = models.TextField(blank=True)
    utilities_included = ArrayField(models.CharField(max_length=50), blank=True)
    available_from = models.DateField()

