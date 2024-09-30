from django.test import TestCase
from properties.models import Property, Address, Amenity, Feature
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class PropertyModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        address = Address.objects.create(
            street="123 Main St",
            zip_code="12345",
            neighborhood_id=1  # Assuming you have a Neighborhood object with id 1
        )
        
        self.property = Property.objects.create(
            title="Test Property",
            description="This is a test property.",
            address=address,
            price=500000.0,
            area=2500.0,
            bedrooms=3,
            bathrooms=2,
            floors=2,
            year_built=2010,
            owner=self.user
        )
        
        self.amenity = Amenity.objects.create(name="Pool")
        self.feature = Feature.objects.create(name="Gym")

    def test_property_creation(self):
        self.assertEqual(self.property.title, "Test Property")
        self.assertEqual(self.property.description, "This is a test property.")
        self.assertEqual(self.property.price, 500000.0)
        self.assertEqual(self.property.area, 2500.0)
        self.assertEqual(self.property.bedrooms, 3)
        self.assertEqual(self.property.bathrooms, 2)
        self.assertEqual(self.property.floors, 2)
        self.assertEqual(self.property.year_built, 2010)
        self.assertEqual(self.property.owner, self.user)

    def test_property_string_representation(self):
        self.assertEqual(str(self.property), "Test Property - 123 Main St")

    def test_property_absolute_url(self):
        url = self.property.get_absolute_url()
        self.assertEqual(url, f'/properties/{self.property.pk}/')

    def test_calculate_price_per_sqft(self):
        price_per_sqft = self.property.calculate_price_per_sqft()
        self.assertAlmostEqual(price_per_sqft, 200.0)

    def test_add_amenity(self):
        PropertyAmenity.objects.create(property=self.property, amenity=self.amenity)
        self.assertEqual(self.property.amenities.count(), 1)

    def test_add_feature(self):
        PropertyFeature.objects.create(property=self.property, feature=self.feature)
        self.assertEqual(self.property.features.count(), 1)

    def test_view_counter(self):
        View.objects.create(property=self.property, user=self.user)
        self.assertEqual(self.property.views.count(), 1)

    def test_favorite_property(self):
        Favorite.objects.create(property=self.property, user=self.user)
        self.assertEqual(self.property.favorites.count(), 1)

    def test_inquiry_creation(self):
        inquiry = Inquiry.objects.create(property=self.property, name="John Doe", email="john@example.com", message="Hello!")
        self.assertEqual(self.property.inquiries.count(), 1)
        self.assertEqual(inquiry.name, "John Doe")
        self.assertEqual(inquiry.email, "john@example.com")
        self.assertEqual(inquiry.message, "Hello!")

    def test_review_creation(self):
        review = Review.objects.create(property=self.property, user=self.user, rating=5, comment="Excellent property!")
        self.assertEqual(self.property.reviews.count(), 1)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent property!")

    def test_property_image_upload(self):
        image_file = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        PropertyImage.objects.create(property=self.property, image=image_file)
        self.assertEqual(self.property.images.count(), 1)

if __name__ == '__main__':
    unittest.main()
