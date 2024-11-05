from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyAttributeViewSet, PropertyImageViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'attributes', PropertyAttributeViewSet, basename='propertyattribute')
router.register(r'images', PropertyImageViewSet, basename='propertyimage')

urlpatterns = [
    path('', include(router.urls)),
]