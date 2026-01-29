"""Admin registration for product-related models.

Contains admin classes and inlines for managing products,
product images and reviews in the Django admin site.
"""

from django.contrib import admin
from .models import Product, ProductImage, ProductReview

class ProductImageInline(admin.TabularInline):
    """Inline admin to manage `ProductImage` objects on the product page."""
    model = ProductImage
    extra = 1

class ProductReviewInline(admin.TabularInline):
    """Inline admin to display `ProductReview` instances; read-only fields."""
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'comment', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin options for `Product` including search, filters and inlines."""
    list_display = ['name', 'sku', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'category', 'brand']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductReviewInline]
    
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Admin for product reviews allowing batch approval action."""
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__email', 'title']
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        """Mark selected reviews as approved."""
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
