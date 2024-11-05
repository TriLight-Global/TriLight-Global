from rest_framework import serializers
from ..properties.models import Property, Address, City, Region, Country, PropertyAttribute, PropertyImage, PropertyAttributeAssignment
from account.models import Agent

# Country Serializer
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']

# Region Serializer
class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = ['id', 'name', 'country']

# City Serializer
class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = City
        fields = ['id', 'name', 'region']

# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Address
        fields = ['id', 'street', 'apartment_number', 'zip_code', 'city', 'latitude', 'longitude']

# Property Attribute Serializer
class PropertyAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAttribute
        fields = ['id', 'name', 'icon', 'attribute_type']

# Property Attribute Assignment Serializer
class PropertyAttributeAssignmentSerializer(serializers.ModelSerializer):
    attribute = PropertyAttributeSerializer()

    class Meta:
        model = PropertyAttributeAssignment
        fields = ['attribute', 'value']

# Property Image Serializer
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_primary', 'caption']

# Property Serializer
class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    attributes = PropertyAttributeAssignmentSerializer(source='attribute_assignments', many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    agents = serializers.SlugRelatedField(slug_field='username', queryset=Agent.objects.all(), many=True)

    class Meta:
        model = Property
        fields = [
            'id', 'uuid', 'title', 'description', 'address', 'property_type', 'status', 'condition',
            'price', 'currency', 'area', 'bedrooms', 'bathrooms', 'floors', 'year_built',
            'last_updated', 'created_at', 'owner', 'featured', 'published', 'attributes', 'images', 'agents'
        ]

    def create(self, validated_data):
        # Handle nested address creation
        address_data = validated_data.pop('address')
        city_data = address_data.pop('city')
        region_data = city_data.pop('region')
        country_data = region_data.pop('country')

        # Ensure nested objects are created or retrieved
        country, _ = Country.objects.get_or_create(**country_data)
        region, _ = Region.objects.get_or_create(country=country, **region_data)
        city, _ = City.objects.get_or_create(region=region, **city_data)
        address, _ = Address.objects.get_or_create(city=city, **address_data)

        # Create the property instance with the resolved address
        property_instance = Property.objects.create(address=address, **validated_data)

        return property_instance

    def update(self, instance, validated_data):
        # Handle updating address if provided
        address_data = validated_data.pop('address', None)
        if address_data:
            city_data = address_data.pop('city', None)
            if city_data:
                region_data = city_data.pop('region', None)
                if region_data:
                    country_data = region_data.pop('country', None)
                    if country_data:
                        country, _ = Country.objects.get_or_create(**country_data)
                        region, _ = Region.objects.get_or_create(country=country, **region_data)
                    else:
                        region = instance.address.city.region
                    city, _ = City.objects.get_or_create(region=region, **city_data)
                else:
                    city = instance.address.city
                address_data['city'] = city
            address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()

        # Update the rest of the fields
        return super().update(instance, validated_data)
