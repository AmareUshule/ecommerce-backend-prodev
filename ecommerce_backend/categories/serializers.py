"""Serializers for category and brand models.

Provides nested category serialization including child categories
and a simple brand serializer for list/detail endpoints.
"""

from rest_framework import serializers
from .models import Category, Brand

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for hierarchical `Category` objects.

    Exposes a `children` field which returns nested child categories when
    present, otherwise returns an empty list.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'image', 
                 'is_active', 'children', 'created_at']
    
    def get_children(self, obj):
        """Return serialized children or an empty list.

        The serializer intentionally materializes child objects here so
        nested representations are returned in the API. This avoids
        exposing a lazy queryset to the response formatters.
        """
        if obj.children.exists():
            # Explicitly evaluate the children queryset for serialization
            return CategorySerializer(obj.children.all(), many=True).data
        return []

class BrandSerializer(serializers.ModelSerializer):
    """Serializer for `Brand` model used by brand endpoints."""
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description', 'logo', 'is_active', 'created_at']
