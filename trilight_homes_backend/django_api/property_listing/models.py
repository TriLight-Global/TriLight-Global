# Properties

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from account.models import Profile
from django.utils.translation import gettext_lazy as _

class AuditFields(models.Model):
    """
    Abstract model that includes audit fields for tracking creation and modification.

    Attributes:
        created_at (DateTimeField): The date and time when the instance was created.
        created_by (ForeignKey): The user who created the instance.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name=_("Created By")
    )

    class Meta:
        abstract = True


class Property(models.Model):
    """
    Model representing a property listing.

    Attributes:
        contractor (ForeignKey): The profile of the contractor managing the property.
        agents (ManyToManyField): Profiles of agents associated with the property.
        staff (ManyToManyField): Profiles of staff members associated with the property.
        buyers (ManyToManyField): Profiles of buyers interested in the property.
        tenant (ForeignKey): The profile of the tenant if the property is rented.
        shareholders (ManyToManyField): Profiles of shareholders for the property.
        board_members (ManyToManyField): Profiles of board members overseeing the property.
        admins (ManyToManyField): Profiles of administrators for the property.
        title (CharField): The title of the property.
        description (TextField): A detailed description of the property.
        property_type (CharField): The type of the property (e.g., apartment, house).
        status (CharField): The current status of the property (e.g., available, sold).
        address (OneToOneField): The address of the property.
        price (DecimalField): The price of the property.
        bedrooms (PositiveIntegerField): The number of bedrooms.
        bathrooms (DecimalField): The number of bathrooms.
        area (DecimalField): The total area of the property in square feet/meters.
        parking_spaces (PositiveIntegerField): The number of parking spaces available.
        features (ArrayField): An array of features associated with the property.
        amenities (ManyToManyField): Amenities available with the property.
        virtual_tour_url (URLField): A URL for a virtual tour of the property.
        energy_rating (CharField): The energy rating of the property.
        listed_date (DateField): The date when the property was listed.
        last_updated (DateTimeField): The date when the property was last updated.
        views_count (PositiveIntegerField): The number of views the property has received.
        is_featured (BooleanField): Whether the property is featured or not.
    """
    class PropertyType(models.TextChoices):
        APARTMENT = 'APARTMENT', _('Apartment')
        HOUSE = 'HOUSE', _('House')
        CONDO = 'CONDO', _('Condominium')
        TOWNHOUSE = 'TOWNHOUSE', _('Townhouse')
        COMMERCIAL = 'COMMERCIAL', _('Commercial')

    class StatusChoices(models.TextChoices):
        AVAILABLE = 'AVAILABLE', _('Available')
        UNDER_CONTRACT = 'UNDER_CONTRACT', _('Under Contract')
        SOLD = 'SOLD', _('Sold')
        RENTED = 'RENTED', _('Rented')
        OFF_MARKET = 'OFF_MARKET', _('Off Market')

    contractor = models.ForeignKey(Profile, related_name='contracted_properties', on_delete=models.SET_NULL, null=True, blank=True)
    agents = models.ManyToManyField(Profile, related_name='agented_properties', blank=True)
    staff = models.ManyToManyField(Profile, related_name='staff_properties', blank=True)
    buyers = models.ManyToManyField(Profile, related_name='bought_properties', blank=True)
    tenant = models.ForeignKey(Profile, related_name='tenant_properties', on_delete=models.SET_NULL, null=True, blank=True)
    shareholders = models.ManyToManyField(Profile, related_name='shared_properties', blank=True)
    board_members = models.ManyToManyField(Profile, related_name='board_properties', blank=True)
    admins = models.ManyToManyField(Profile, related_name='admin_properties', blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PropertyType.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.AVAILABLE)
    address = models.OneToOneField('Address', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    area = models.DecimalField(max_digits=10, decimal_places=2)  # in square feet/meters
    parking_spaces = models.PositiveIntegerField(default=0)
    features = ArrayField(models.CharField(max_length=100), blank=True)
    amenities = models.ManyToManyField('Amenity', related_name='properties', blank=True)
    virtual_tour_url = models.URLField(blank=True)
    energy_rating = models.CharField(max_length=10, blank=True)

    # Audit fields
    listed_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Address(AuditFields):
    """
    Model representing the address of a property.

    Attributes:
        street (CharField): The street address.
        city (CharField): The city of the address.
        state (CharField): The state of the address.
        zip_code (CharField): The ZIP or postal code.
        country (CharField): The country of the address.
        latitude (DecimalField): The latitude of the property location.
        longitude (DecimalField): The longitude of the property location.
    """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"


class Amenity(AuditFields):
    """
    Model representing an amenity available with a property.

    Attributes:
        name (CharField): The name of the amenity.
        description (TextField): A description of the amenity.
        icon (CharField): The CSS class or icon name representing the amenity.
    """
    AmenityChoices = [
        ('SWIMMING_POOL', 'Swimming Pool'),
        ('GYM', 'Gym'),
        ('GARDEN', 'Garden'),
        ('SECURITY', '24/7 Security'),
        ('PARKING', 'Parking Space'),
        ('PLAYGROUND', 'Playground'),
        ('BALCONY', 'Balcony'),
        ('TERRACE', 'Terrace'),
        ('BACKUP_GENERATOR', 'Backup Generator'),
        ('SOLAR_POWER', 'Solar Power'),
        ('BOREHOLE', 'Borehole'),
        ('CCTV', 'CCTV Surveillance'),
        ('AIR_CONDITIONING', 'Air Conditioning'),
        ('WIFI', 'Wi-Fi'),
        ('DSTV_CONNECTION', 'DSTV Connection'),
        ('FIREPLACE', 'Fireplace'),
        ('FURNISHED', 'Furnished'),
        ('UNFURNISHED', 'Unfurnished'),
        ('CLOSET_SPACE', 'Closet Space'),
        ('GATED_COMMUNITY', 'Gated Community'),
        ('SERVANT_QUARTERS', 'Servant Quarters'),
        ('LAUNDRY_ROOM', 'Laundry Room'),
        ('STORAGE', 'Storage Room'),
        ('ROOFTOP', 'Rooftop Access'),
        ('BBQ_AREA', 'BBQ Area'),
        ('CONFERENCE_ROOM', 'Conference Room'),
        ('LOUNGE', 'Lounge'),
        ('ELEVATOR', 'Elevator'),
        ('DISABLED_ACCESS', 'Disabled Access'),
        ('BUSINESS_CENTER', 'Business Center'),
        ('WATER_TREATMENT', 'Water Treatment System'),
        ('CLUBHOUSE', 'Clubhouse'),
        ('SPA', 'Spa'),
        ('TENNIS_COURT', 'Tennis Court'),
        ('BASKETBALL_COURT', 'Basketball Court'),
        ('SHOPPING_CENTER', 'Shopping Center Nearby'),
        ('RESTAURANT', 'On-site Restaurant'),
        ('CLINIC', 'Clinic Nearby'),
        ('SCHOOL', 'School Nearby'),
    ]

    name = models.CharField(max_length=50, choices=AmenityChoices, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # CSS class or icon name

    def __str__(self):
        return self.get_name_display()


class PropertyImage(AuditFields):
    """
    Model representing images associated with a property.

    Attributes:
        property (ForeignKey): The property the image is associated with.
        image (ImageField): The image file.
        caption (CharField): An optional caption for the image.
        is_primary (BooleanField): Indicates if this is the primary image for the property.
        order (PositiveIntegerField): The display order of the image.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)


class PropertyHistory(AuditFields):
    """
    Model representing the history of changes made to a property.

    Attributes:
        property (ForeignKey): The property the history is associated with.
        event_type (CharField): The type of event (e.g., price change, status change).
        event_date (DateTimeField): The date and time of the event.
        description (TextField): A description of the event.
        old_value (CharField): The old value before the event.
        new_value (CharField): The new value after the event.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='history')
    event_type = models.CharField(max_length=50)  # e.g., 'PRICE_CHANGE', 'STATUS_CHANGE'
    event_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)


class PropertyReview(AuditFields):
    """
    Model representing a review of a property.

    Attributes:
        property (ForeignKey): The property being reviewed.
        reviewer (ForeignKey): The user who wrote the review.
        rating (PositiveIntegerField): The rating given to the property.
        comment (TextField): The review comment.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()


class PropertyView(AuditFields):
    """
    Model representing a view of a property.

    Attributes:
        property (ForeignKey): The property that was viewed.
        viewer (ForeignKey): The user who viewed the property.
        view_date (DateTimeField): The date and time of the view.
        ip_address (GenericIPAddressField): The IP address of the viewer.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_views')
    viewer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    view_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)


class FavoriteProperty(AuditFields):
    """
    Model representing a user's favorite property.

    Attributes:
        user (ForeignKey): The user who marked the property as favorite.
        property (ForeignKey): The property that was favorited.
        added_date (DateTimeField): The date and time when the property was added to favorites.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorite_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    added_date = models.DateTimeField(auto_now_add=True)


class PropertyInquiry(AuditFields):
    """
    Model representing an inquiry about a property.

    Attributes:
        property (ForeignKey): The property being inquired about.
        inquirer (ForeignKey): The user making the inquiry.
        message (TextField): The inquiry message.
        contact_phone (CharField): The contact phone number.
        contact_email (EmailField): The contact email address.
        responded (BooleanField): Indicates if the inquiry has been responded to.
        response_date (DateTimeField): The date and time of the response.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    inquirer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='property_inquiries')
    message = models.TextField()
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField()
    responded = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)


class PropertyValuation(AuditFields):
    """
    Model representing a valuation of a property.

    Attributes:
        property (ForeignKey): The property being valued.
        valuation_date (DateField): The date of the valuation.
        valuation_amount (DecimalField): The amount of the valuation.
        valuer (ForeignKey): The user who conducted the valuation.
        valuation_method (CharField): The method used for the valuation.
        notes (TextField): Any additional notes regarding the valuation.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='valuations')
    valuation_date = models.DateField()
    valuation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    valuer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    valuation_method = models.CharField(max_length=100)
    notes = models.TextField(blank=True)


class PropertyTax(AuditFields):
    """
    Model representing the tax information for a property.

    Attributes:
        property (ForeignKey): The property associated with the tax.
        tax_year (PositiveIntegerField): The year the tax applies to.
        amount (DecimalField): The amount of the tax.
        paid (BooleanField): Indicates if the tax has been paid.
        due_date (DateField): The due date for the tax payment.
        payment_date (DateField): The date the payment was made.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='taxes')
    tax_year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)


class PropertyInsurance(AuditFields):
    """
    Model representing insurance information for a property.

    Attributes:
        property (ForeignKey): The property associated with the insurance.
        insurance_provider (CharField): The name of the insurance provider.
        policy_number (CharField): The policy number of the insurance.
        coverage_amount (DecimalField): The amount covered by the insurance.
        premium (DecimalField): The premium for the insurance policy.
        start_date (DateField): The start date of the insurance coverage.
        end_date (DateField): The end date of the insurance coverage.
        is_active (BooleanField): Indicates if the insurance is currently active.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='insurances')
    insurance_provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


class PropertyMortgage(AuditFields):
    """
    Model representing mortgage information for a property.

    Attributes:
        property (ForeignKey): The property associated with the mortgage.
        lender (CharField): The name of the lender.
        loan_amount (DecimalField): The amount of the loan.
        interest_rate (DecimalField): The interest rate of the mortgage.
        term_years (PositiveIntegerField): The term of the mortgage in years.
        start_date (DateField): The start date of the mortgage.
        monthly_payment (DecimalField): The monthly payment amount.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='mortgages')
    lender = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_years = models.PositiveIntegerField()
    start_date = models.DateField()
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)


class OpenHouse(AuditFields):
    """
    Model representing an open house event for a property.

    Attributes:
        property (ForeignKey): The property associated with the open house.
        start_time (DateTimeField): The start time of the open house.
        end_time (DateTimeField): The end time of the open house.
        description (TextField): A description of the open house event.
    
    Meta:
        unique_together: ('property', 'start_time')
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='open_houses')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('property', 'start_time')


class PropertyListing(AuditFields):
    """
    Model representing a listing for a property.

    Attributes:
        property (OneToOneField): The property being listed.
        listing_type (CharField): The type of listing (for sale, for rent, auction).
        list_date (DateField): The date the property was listed.
        list_price (DecimalField): The listing price of the property.
        listing_agent (ForeignKey): The agent responsible for the listing.
        commission_percentage (DecimalField): The commission percentage for the agent.
        listing_description (TextField): A description of the listing.
        showing_instructions (TextField): Instructions for showing the property.
    """
    LISTING_TYPES = [
        ('FOR_SALE', 'For Sale'),
        ('FOR_RENT', 'For Rent'),
        ('AUCTION', 'Auction'),
    ]

    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='listing')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    list_date = models.DateField(auto_now_add=True)
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_agent = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='property_listings')
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    listing_description = models.TextField(blank=True)
    showing_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.property.title} - {self.get_listing_type_display()}"


class PropertyLease(AuditFields):
    """
    Model representing a lease agreement for a property.

    Attributes:
        property (ForeignKey): The property being leased.
        tenant (ForeignKey): The tenant leasing the property.
        lease_start_date (DateField): The start date of the lease.
        lease_end_date (DateField): The end date of the lease.
        monthly_rent (DecimalField): The monthly rent for the property.
        security_deposit (DecimalField): The security deposit amount.
        lease_terms (TextField): Specific terms of the lease agreement.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='leases')
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    lease_terms = models.TextField(blank=True)

    def __str__(self):
        return f"Lease for {self.property.title} by {self.tenant.user.username}"


class PropertyContract(AuditFields):
    """
    Model representing a contract for a property transaction.

    Attributes:
        property (ForeignKey): The property associated with the contract.
        buyer (ForeignKey): The buyer involved in the transaction.
        seller (ForeignKey): The seller involved in the transaction.
        contract_date (DateField): The date the contract was signed.
        contract_terms (TextField): The terms of the contract.
        status (CharField): Current status of the contract (e.g., active, completed, cancelled).
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contracts')
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchase_contracts')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sale_contracts')
    contract_date = models.DateField()
    contract_terms = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"Contract for {self.property.title} between {self.seller.user.username} and {self.buyer.user.username}"


class PropertyEvent(AuditFields):
    """
    Model representing events related to a property.

    Attributes:
        property (ForeignKey): The property associated with the event.
        event_type (CharField): Type of event (e.g., showing, open house, inspection).
        event_date (DateTimeField): The date and time of the event.
        description (TextField): A description of the event.
    """
    EVENT_TYPES = [
        ('SHOWING', 'Showing'),
        ('OPEN_HOUSE', 'Open House'),
        ('INSPECTION', 'Inspection'),
        ('OTHER', 'Other'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_event_type_display()} for {self.property.title} on {self.event_date.strftime('%Y-%m-%d %H:%M')}"


class PropertyDisclosure(AuditFields):
    """
    Model representing disclosures related to a property.

    Attributes:
        property (ForeignKey): The property associated with the disclosure.
        disclosure_date (DateField): The date of the disclosure.
        disclosure_description (TextField): A description of the disclosure.
        is_disclosed (BooleanField): Indicates if the disclosure has been acknowledged.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='disclosures')
    disclosure_date = models.DateField()
    disclosure_description = models.TextField()
    is_disclosed = models.BooleanField(default=False)

    def __str__(self):
        return f"Disclosure for {self.property.title} on {self.disclosure_date.strftime('%Y-%m-%d')}"

