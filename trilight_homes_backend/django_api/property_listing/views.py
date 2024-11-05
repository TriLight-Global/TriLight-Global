from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PropertySerializer, PropertyAttributeSerializer, PropertyImageSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from mongodb import get_collection
from bson import ObjectId

@extend_schema_view(
    list=extend_schema(description='List all properties'),
    retrieve=extend_schema(description='Retrieve a property by ID'),
    create=extend_schema(description='Create a new property'),
    update=extend_schema(description='Update an existing property'),
    partial_update=extend_schema(description='Partially update an existing property'),
    destroy=extend_schema(description='Delete a property')
)
class PropertyViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        properties_collection = get_collection('properties')
        return list(properties_collection.find())
    
    def list(self, request):
        properties = self.get_queryset()
        return Response(PropertySerializer(properties, many=True).data)

    def retrieve(self, request, pk=None):
        properties_collection = get_collection('properties')
        property_data = properties_collection.find_one({'_id': ObjectId(pk)})
        if property_data:
            return Response(PropertySerializer(property_data).data)
        return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        properties_collection = get_collection('properties')
        data = request.data
        data['owner'] = str(request.user.id)
        result = properties_collection.insert_one(data)
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create property'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        properties_collection = get_collection('properties')
        result = properties_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property updated'})
        return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        properties_collection = get_collection('properties')
        result = properties_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property partially updated'})
        return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        properties_collection = get_collection('properties')
        result = properties_collection.delete_one({'_id': ObjectId(pk)})
        if result.deleted_count > 0:
            return Response({'status': 'Property deleted'})
        return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='add-attribute')
    @extend_schema(
        description='Add an attribute to a property',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'attribute_id': {'type': 'string'},
                    'value': {'type': 'string'}
                },
                'required': ['attribute_id'],
                'additionalProperties': False,
            }
        },
        responses={201: None},
        auth=[],
    )
    def add_attribute(self, request, pk=None):
        properties_collection = get_collection('properties')
        property_data = properties_collection.find_one({'_id': ObjectId(pk)})
        if not property_data:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

        attribute_id = request.data.get('attribute_id')
        value = request.data.get('value', '')

        attributes_collection = get_collection('property_attributes')
        attribute = attributes_collection.find_one({'_id': ObjectId(attribute_id)})

        if attribute:
            result = properties_collection.update_one(
                {'_id': ObjectId(pk)},
                {'$push': {'attributes': {'attribute_id': attribute_id, 'value': value}}}
            )
            if result.modified_count > 0:
                return Response({'status': 'Attribute added'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'Failed to add attribute'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Attribute not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='add-image')
    @extend_schema(
        description='Add an image to a property',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {'type': 'string', 'format': 'binary'},
                    'caption': {'type': 'string'}
                },
                'required': ['image'],
                'additionalProperties': False,
            }
        },
        responses={201: PropertyImageSerializer},
        auth=[],
    )
    def add_image(self, request, pk=None):
        properties_collection = get_collection('properties')
        property_data = properties_collection.find_one({'_id': ObjectId(pk)})

        if not property_data:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

        # Note: You'll need to implement image saving logic here
        # This is a placeholder for where you'd handle the file upload
        image_data = {
            'image': 'path/to/saved/image.jpg',  # Replace with actual image saving logic
            'caption': request.data.get('caption', ''),
            'property_id': str(pk)
        }

        images_collection = get_collection('property_images')
        result = images_collection.insert_one(image_data)
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to add image'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    list=extend_schema(description='List all property attributes'),
    retrieve=extend_schema(description='Retrieve a property attribute by ID'),
    create=extend_schema(description='Create a new property attribute'),
    update=extend_schema(description='Update an existing property attribute'),
    partial_update=extend_schema(description='Partially update an existing property attribute'),
    destroy=extend_schema(description='Delete a property attribute')
)
class PropertyAttributeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        attributes_collection = get_collection('property_attributes')
        return list(attributes_collection.find())

    def list(self, request):
        attributes = self.get_queryset()
        return Response(PropertyAttributeSerializer(attributes, many=True).data)

    def retrieve(self, request, pk=None):
        attributes_collection = get_collection('property_attributes')
        attribute_data = attributes_collection.find_one({'_id': ObjectId(pk)})
        if attribute_data:
            return Response(PropertyAttributeSerializer(attribute_data).data)
        return Response({'error': 'Attribute not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        attributes_collection = get_collection('property_attributes')
        result = attributes_collection.insert_one(request.data)
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create attribute'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        attributes_collection = get_collection('property_attributes')
        result = attributes_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property attribute updated'})
        return Response({'error': 'Attribute not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        attributes_collection = get_collection('property_attributes')
        result = attributes_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property attribute partially updated'})
        return Response({'error': 'Attribute not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        attributes_collection = get_collection('property_attributes')
        result = attributes_collection.delete_one({'_id': ObjectId(pk)})
        if result.deleted_count > 0:
            return Response({'status': 'Property attribute deleted'})
        return Response({'error': 'Attribute not found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema_view(
    list=extend_schema(description='List all property images'),
    retrieve=extend_schema(description='Retrieve a property image by ID'),
    create=extend_schema(description='Create a new property image'),
    update=extend_schema(description='Update an existing property image'),
    partial_update=extend_schema(description='Partially update an existing property image'),
    destroy=extend_schema(description='Delete a property image')
)
class PropertyImageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        images_collection = get_collection('property_images')
        return list(images_collection.find())

    def list(self, request):
        images = self.get_queryset()
        return Response(PropertyImageSerializer(images, many=True).data)

    def retrieve(self, request, pk=None):
        images_collection = get_collection('property_images')
        image_data = images_collection.find_one({'_id': ObjectId(pk)})
        if image_data:
            return Response(PropertyImageSerializer(image_data).data)
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        images_collection = get_collection('property_images')
        # Note: You'll need to implement image saving logic here
        # This is a placeholder for where you'd handle the file upload
        image_data = {
            'image': 'path/to/saved/image.jpg',  # Replace with actual image saving logic
            'caption': request.data.get('caption', ''),
            'property_id': request.data.get('property_id')
        }
        result = images_collection.insert_one(image_data)
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create image'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        images_collection = get_collection('property_images')
        result = images_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property image updated'})
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        images_collection = get_collection('property_images')
        result = images_collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
        if result.modified_count > 0:
            return Response({'status': 'Property image partially updated'})
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        images_collection = get_collection('property_images')
        result = images_collection.delete_one({'_id': ObjectId(pk)})
        if result.deleted_count > 0:
            return Response({'status': 'Property image deleted'})
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)