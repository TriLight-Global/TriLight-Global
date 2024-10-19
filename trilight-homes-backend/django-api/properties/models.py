from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import uuid

from account.models import Agent, Agency

# Currency Choices
class Currency(models.IntegerChoices):
    USD = 1, _("US Dollar")
    EUR = 2, _("Euro")
    GBP = 3, _("British Pound")
    NGA = 4, _("Naira")
    GHC = 5, _("Ghana Cedis")

# Property Types Choices
class PropertyType(models.IntegerChoices):
    STUDIO_APARTMENT = 1, _("Studio Apartment")
    LOFT_APARTMENT = 2, _("Loft Apartment")
    PENTHOUSE_APARTMENT = 3, _("Penthouse Apartment")
    DETACHED_HOUSE = 4, _("Detached House")
    SEMI_DETACHED_HOUSE = 5, _("Semi-detached House")
    BUNGALOW = 6, _("Bungalow")
    COTTAGE = 7, _("Cottage")
    VILLA = 8, _("Villa")
    HIGH_RISE_CONDO = 9, _("High-rise Condo")
    LOW_RISE_CONDO = 10, _("Low-rise Condo")
    ROW_TOWNHOUSE = 11, _("Row Townhouse")
    END_UNIT_TOWNHOUSE = 12, _("End-unit Townhouse")
    RESIDENTIAL_LAND = 13, _("Residential Land")
    COMMERCIAL_LAND = 14, _("Commercial Land")
    AGRICULTURAL_LAND = 15, _("Agricultural Land")
    INDUSTRIAL_LAND = 16, _("Industrial Land")

# Property Status Choices
class PropertyStatus(models.IntegerChoices):
    FOR_SALE = 1, _("For Sale")
    SOLD = 2, _("Sold")
    RENTAL = 3, _("Rental")
    LEASED = 4, _("Leased")
    UNAVAILABLE = 5, _("Unavailable")

# Property Condition Choices
class PropertyCondition(models.IntegerChoices):
    NEW = 1, _("New")
    USED = 2, _("Used")
    RENOVATED = 3, _("Renovated")

# Property Model
class Property(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    property_type = models.IntegerField(_("Property Type"), choices=PropertyType.choices, default=PropertyType.STUDIO_APARTMENT)
    status = models.IntegerField(_("Status"), choices=PropertyStatus.choices, default=PropertyStatus.FOR_SALE)
    condition = models.IntegerField(_("Condition"), choices=PropertyCondition.choices, default=PropertyCondition.USED)
    price = models.DecimalField(_("Price"), max_digits=15, decimal_places=2)
    currency = models.IntegerField(_("Currency"), choices=Currency.choices, default=Currency.USD)
    area = models.DecimalField(_("Area"), max_digits=10, decimal_places=2, help_text=_("in square meters"))
    bedrooms = models.IntegerField(_("Bedrooms"))
    bathrooms = models.IntegerField(_("Bathrooms"))
    floors = models.IntegerField(_("Floors"))
    year_built = models.IntegerField(_("Year Built"))
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    featured = models.BooleanField(_("Featured"), default=False)
    features = ArrayField(models.CharField(max_length=100), blank=True)
    virtual_tour_url = models.URLField(blank=True)
    published = models.BooleanField(_("Published"), default=False)
    attributes = models.ManyToManyField('PropertyAttribute', through='PropertyAttributeAssignment')
    agents = models.ManyToManyField(Agent, related_name='listed_properties')

    def __str__(self):
        return f"{self.title} - {self.address}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('property_detail', kwargs={'pk': self.pk})

    def calculate_price_per_sqft(self):
        return self.price / self.area if self.area > 0 else 0

# Address Model
class Address(models.Model):
    street = models.CharField(_("Street"), max_length=255)
    apartment_number = models.CharField(_("Apartment Number"), max_length=20, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=20)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    latitude = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}"

    def get_full_address(self):
        return f"{self.street}, Apt {self.apartment_number}, {self.zip_code}, {self.city.name}, {self.city.region.name}, {self.city.region.country.name}"

# City Model
class City(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Region Model
class Region(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Country Model
class Country(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=2)  # ISO country code

    def __str__(self):
        return self.name

# Property Attribute Model
class PropertyAttribute(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    icon = models.CharField(_("Icon"), max_length=50, blank=True)
    attribute_type = models.CharField(_("Type"), max_length=20, choices=[('amenity', 'Amenity'), ('feature', 'Feature')])

    def __str__(self):
        return f"{self.get_attribute_type_display()}: {self.name}"

# Property Attribute Assignment Model
class PropertyAttributeAssignment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='attribute_assignments')
    attribute = models.ForeignKey(PropertyAttribute, on_delete=models.CASCADE)
    value = models.CharField(_("Value"), max_length=100, blank=True)  # For quantitative or descriptive attributes

    def __str__(self):
        return f"{self.property.title} - {self.attribute.name}: {self.value}"

# Property Activity Model
class PropertyActivity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_activities')
    activity_type = models.CharField(_("Activity Type"), max_length=20, choices=[
        ('view', 'View'),
        ('favorite', 'Favorite'),
        ('inquiry', 'Inquiry'),
        ('review', 'Review')
    ])
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    details = models.JSONField(_("Details"), default=dict)  # Stores activity-specific details

    def __str__(self):
        return f"{self.get_activity_type_display()} on {self.property.title} by {self.user.username}"

# Property Image Model
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_("Image"), upload_to='property_images/')
    is_primary = models.BooleanField(_("Is Primary"), default=False)
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}: {'Primary' if self.is_primary else 'Secondary'}"

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_params = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Viewing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='agent_viewings')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20)
