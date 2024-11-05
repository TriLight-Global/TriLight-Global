from django.test import TestCase
from django.contrib.auth import get_user_model
from django_api.property_listing.models import (
    Property, Address, Amenity, PropertyImage, PropertyHistory, 
    PropertyReview, PropertyView, FavoriteProperty, PropertyInquiry, 
    PropertyValuation, PropertyTax, PropertyInsurance, PropertyMortgage, 
    OpenHouse, PropertyListing, PropertyLease, PropertyContract, 
    PropertyEvent, PropertyDisclosure
)
from account.models import Profile

class PropertyModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )

    def test_property_creation(self):
        """Test that a Property instance is created correctly."""
        self.assertEqual(self.property.title, 'Test Property')
        self.assertEqual(self.property.price, 300000.00)

    def test_property_str(self):
        """Test the string representation of Property."""
        self.assertEqual(str(self.property), 'Test Property')


class AddressModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street='123 Main St',
            city='Springfield',
            state='IL',
            zip_code='62701',
            country='USA'
        )

    def test_address_creation(self):
        """Test that an Address instance is created correctly."""
        self.assertEqual(self.address.street, '123 Main St')
        self.assertEqual(self.address.city, 'Springfield')

    def test_address_str(self):
        """Test the string representation of Address."""
        self.assertEqual(str(self.address), '123 Main St, Springfield, IL 62701, USA')


class AmenityModelTest(TestCase):
    def setUp(self):
        self.amenity = Amenity.objects.create(
            name='SWIMMING_POOL',
            description='A large swimming pool',
            icon='pool-icon'
        )

    def test_amenity_creation(self):
        """Test that an Amenity instance is created correctly."""
        self.assertEqual(self.amenity.name, 'SWIMMING_POOL')

    def test_amenity_str(self):
        """Test the string representation of Amenity."""
        self.assertEqual(str(self.amenity), 'Swimming Pool')


class PropertyImageModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_image = PropertyImage.objects.create(
            property=self.property,
            image='path/to/image.jpg',
            caption='Test Image',
            is_primary=True
        )

    def test_property_image_creation(self):
        """Test that a PropertyImage instance is created correctly."""
        self.assertEqual(self.property_image.caption, 'Test Image')

    def test_property_image_str(self):
        """Test the string representation of PropertyImage."""
        self.assertEqual(str(self.property_image), 'Test Image')


class PropertyHistoryModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.history = PropertyHistory.objects.create(
            property=self.property,
            event_type='PRICE_CHANGE',
            description='Price changed from 250000 to 300000',
            old_value='250000',
            new_value='300000'
        )

    def test_property_history_creation(self):
        """Test that a PropertyHistory instance is created correctly."""
        self.assertEqual(self.history.event_type, 'PRICE_CHANGE')

    def test_property_history_str(self):
        """Test the string representation of PropertyHistory."""
        self.assertEqual(str(self.history), 'PRICE_CHANGE')


class PropertyReviewModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.review = PropertyReview.objects.create(
            property=self.property,
            reviewer=self.agent_user,
            rating=5,
            comment='Great property!'
        )

    def test_property_review_creation(self):
        """Test that a PropertyReview instance is created correctly."""
        self.assertEqual(self.review.rating, 5)

    def test_property_review_str(self):
        """Test the string representation of PropertyReview."""
        self.assertEqual(str(self.review), 'Great property!')


class PropertyViewModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_view = PropertyView.objects.create(
            property=self.property,
            viewer=self.agent_user,
            ip_address='192.168.1.1'
        )

    def test_property_view_creation(self):
        """Test that a PropertyView instance is created correctly."""
        self.assertEqual(self.property_view.ip_address, '192.168.1.1')

    def test_property_view_str(self):
        """Test the string representation of PropertyView."""
        self.assertEqual(str(self.property_view), str(self.property))


class FavoritePropertyModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.favorite = FavoriteProperty.objects.create(
            user=self.agent_user,
            property=self.property
        )

    def test_favorite_property_creation(self):
        """Test that a FavoriteProperty instance is created correctly."""
        self.assertEqual(self.favorite.user, self.agent_user)

    def test_favorite_property_str(self):
        """Test the string representation of FavoriteProperty."""
        self.assertEqual(str(self.favorite), str(self.property))


class PropertyInquiryModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.inquiry = PropertyInquiry.objects.create(
            property=self.property,
            inquirer=self.agent_user,
            message='I am interested in this property.',
            contact_email='test@example.com'
        )

    def test_property_inquiry_creation(self):
        """Test that a PropertyInquiry instance is created correctly."""
        self.assertEqual(self.inquiry.message, 'I am interested in this property.')

    def test_property_inquiry_str(self):
        """Test the string representation of PropertyInquiry."""
        self.assertEqual(str(self.inquiry), 'I am interested in this property.')


class PropertyValuationModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.valuation = PropertyValuation.objects.create(
            property=self.property,
            estimated_value=320000.00,
            valuation_date='2024-01-01',
            appraiser=self.agent_user
        )

    def test_property_valuation_creation(self):
        """Test that a PropertyValuation instance is created correctly."""
        self.assertEqual(self.valuation.estimated_value, 320000.00)

    def test_property_valuation_str(self):
        """Test the string representation of PropertyValuation."""
        self.assertEqual(str(self.valuation), '320000.00')


class PropertyTaxModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_tax = PropertyTax.objects.create(
            property=self.property,
            amount=3000.00,
            due_date='2024-04-15',
            paid=False
        )

    def test_property_tax_creation(self):
        """Test that a PropertyTax instance is created correctly."""
        self.assertEqual(self.property_tax.amount, 3000.00)

    def test_property_tax_str(self):
        """Test the string representation of PropertyTax."""
        self.assertEqual(str(self.property_tax), '3000.00')


class PropertyInsuranceModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_insurance = PropertyInsurance.objects.create(
            property=self.property,
            provider='Best Insurance Co.',
            policy_number='POL123456',
            coverage_amount=250000.00,
            premium=1200.00
        )

    def test_property_insurance_creation(self):
        """Test that a PropertyInsurance instance is created correctly."""
        self.assertEqual(self.property_insurance.provider, 'Best Insurance Co.')

    def test_property_insurance_str(self):
        """Test the string representation of PropertyInsurance."""
        self.assertEqual(str(self.property_insurance), 'POL123456')


class PropertyMortgageModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_mortgage = PropertyMortgage.objects.create(
            property=self.property,
            lender='XYZ Bank',
            amount=200000.00,
            interest_rate=3.5,
            term_years=30
        )

    def test_property_mortgage_creation(self):
        """Test that a PropertyMortgage instance is created correctly."""
        self.assertEqual(self.property_mortgage.amount, 200000.00)

    def test_property_mortgage_str(self):
        """Test the string representation of PropertyMortgage."""
        self.assertEqual(str(self.property_mortgage), '200000.00')


class OpenHouseModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.open_house = OpenHouse.objects.create(
            property=self.property,
            date='2024-05-01',
            start_time='14:00',
            end_time='16:00',
            description='Open house event for potential buyers.'
        )

    def test_open_house_creation(self):
        """Test that an OpenHouse instance is created correctly."""
        self.assertEqual(self.open_house.description, 'Open house event for potential buyers.')

    def test_open_house_str(self):
        """Test the string representation of OpenHouse."""
        self.assertEqual(str(self.open_house), 'Open house event for potential buyers.')


class PropertyListingModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_listing = PropertyListing.objects.create(
            property=self.property,
            listing_date='2024-01-01',
            expiration_date='2024-12-31',
            listing_price=305000.00
        )

    def test_property_listing_creation(self):
        """Test that a PropertyListing instance is created correctly."""
        self.assertEqual(self.property_listing.listing_price, 305000.00)

    def test_property_listing_str(self):
        """Test the string representation of PropertyListing."""
        self.assertEqual(str(self.property_listing), '305000.00')


class PropertyLeaseModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='LEASE',
            status='AVAILABLE',
            price=1500.00,
            bedrooms=2,
            bathrooms=1.0,
            area=900.00,
            listing_agent=self.agent_profile
        )
        self.property_lease = PropertyLease.objects.create(
            property=self.property,
            monthly_rent=1500.00,
            lease_start_date='2024-01-01',
            lease_end_date='2025-01-01'
        )

    def test_property_lease_creation(self):
        """Test that a PropertyLease instance is created correctly."""
        self.assertEqual(self.property_lease.monthly_rent, 1500.00)

    def test_property_lease_str(self):
        """Test the string representation of PropertyLease."""
        self.assertEqual(str(self.property_lease), '1500.00')


class PropertyContractModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_contract = PropertyContract.objects.create(
            property=self.property,
            contract_date='2024-01-01',
            contract_terms='Standard purchase agreement terms',
            buyer=self.agent_user
        )

    def test_property_contract_creation(self):
        """Test that a PropertyContract instance is created correctly."""
        self.assertEqual(self.property_contract.contract_terms, 'Standard purchase agreement terms')

    def test_property_contract_str(self):
        """Test the string representation of PropertyContract."""
        self.assertEqual(str(self.property_contract), 'Standard purchase agreement terms')


class PropertyEventModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_event = PropertyEvent.objects.create(
            property=self.property,
            event_date='2024-05-01',
            event_type='Open House',
            description='Open house event for potential buyers.'
        )

    def test_property_event_creation(self):
        """Test that a PropertyEvent instance is created correctly."""
        self.assertEqual(self.property_event.event_type, 'Open House')

    def test_property_event_str(self):
        """Test the string representation of PropertyEvent."""
        self.assertEqual(str(self.property_event), 'Open House')


class PropertyDisclosureModelTest(TestCase):
    def setUp(self):
        self.agent_user = get_user_model().objects.create_user(
            username='agent1',
            password='password123'
        )
        self.agent_profile = Profile.objects.create(user=self.agent_user)
        self.property = Property.objects.create(
            title='Test Property',
            description='A description for the test property.',
            property_type='HOUSE',
            status='AVAILABLE',
            price=300000.00,
            bedrooms=3,
            bathrooms=2.0,
            area=1500.00,
            listing_agent=self.agent_profile
        )
        self.property_disclosure = PropertyDisclosure.objects.create(
            property=self.property,
            disclosure_text='There has been water damage in the past.',
            date_disclosed='2024-01-01'
        )

    def test_property_disclosure_creation(self):
        """Test that a PropertyDisclosure instance is created correctly."""
        self.assertEqual(self.property_disclosure.disclosure_text, 'There has been water damage in the past.')

    def test_property_disclosure_str(self):
        """Test the string representation of PropertyDisclosure."""
        self.assertEqual(str(self.property_disclosure), 'There has been water damage in the past.')
