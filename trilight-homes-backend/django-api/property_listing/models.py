# Property Listing App

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('commercial', 'Commercial'),
    ])
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_footage = models.PositiveIntegerField()
    year_built = models.PositiveIntegerField()
    listing_status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
        ('off_market', 'Off Market'),
    ])
    listing_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

class PropertyDocument(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='property_documents/')
    document_type = models.CharField(max_length=50, choices=[
        ('deed', 'Deed'),
        ('tax_record', 'Tax Record'),
        ('floor_plan', 'Floor Plan'),
        ('inspection_report', 'Inspection Report'),
    ])
    upload_date = models.DateTimeField(auto_now_add=True)

class Amenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class PropertyHistory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='history')
    event_type = models.CharField(max_length=50, choices=[
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('renovation', 'Renovation'),
        ('listing', 'Listing'),
        ('price_change', 'Price Change'),
    ])
    event_date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
