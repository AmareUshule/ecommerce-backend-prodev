"""Serializers for product models and API representations.

This module defines serializers used by the products API: full and
list representations for `Product`, plus serializers for `ProductImage`
and `ProductReview` used by nested representations.
"""

from rest_framework import serializers
from .models import Product, ProductImage, ProductReview
from categories.serializers import CategorySerializer, BrandSerializer
from categories.models import Category, Brand

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for `ProductImage` model."""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']

class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for `ProductReview` model.

    Exposes the reviewer as a readable string and marks the `user`
    and approval fields as read-only for API-created reviews.
    """
    user = serializers.StringRelatedField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'title', 'comment', 'is_approved', 'created_at']
        read_only_fields = ['user', 'is_approved']

class ProductSerializer(serializers.ModelSerializer):
    """Detailed serializer for `Product` including relations.

    Includes nested `Category`, `Brand`, `images` and `reviews`.
    Accepts `category_id`/`brand_id` for writes while keeping nested
    representations read-only.
    """
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True, required=False
    )
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'description', 'price', 'discounted_price',
                 'final_price', 'category', 'category_id', 'brand', 'brand_id',
                 'stock_quantity', 'images', 'reviews', 'is_active', 'is_featured',
                 'created_at', 'updated_at']
        read_only_fields = ['slug', 'final_price']

class ProductListSerializer(serializers.ModelSerializer):
    """Compact serializer used for product listing endpoints.

    Exposes a `primary_image` helper field and lightweight
    category/brand string fields for faster list responses.
    """
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    primary_image = serializers.SerializerMethodField()
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'price', 'discounted_price', 'final_price',
                 'category', 'brand', 'stock_quantity', 'primary_image', 'is_featured']
    
    def get_primary_image(self, obj):
        """Return the URL of the primary image or `None` if missing."""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None
