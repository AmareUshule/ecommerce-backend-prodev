"""Views for category and brand endpoints.

Provides public listing/detail views and admin-only create/update/delete
endpoints for categories and brands. Category listing returns only top
level categories by default.
"""

from rest_framework import generics, permissions
from django.db.models import Count
from .models import Category, Brand
from .serializers import CategorySerializer, BrandSerializer

class CategoryListView(generics.ListAPIView):
    """List top-level categories (parent is None) for public consumption."""
    queryset = Category.objects.filter(is_active=True, parent=None)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CategoryDetailView(generics.RetrieveAPIView):
    """Retrieve a single category by slug (public)."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class BrandListView(generics.ListAPIView):
    """List active brands."""
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]

class CategoryCreateView(generics.CreateAPIView):
    """Admin-only endpoint to create categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class BrandCreateView(generics.CreateAPIView):
    """Admin-only endpoint to create brands."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryUpdateView(generics.UpdateAPIView):
    """Admin view to update a category identified by slug."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

class CategoryDeleteView(generics.DestroyAPIView):
    """Admin view to delete a category identified by slug."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

class BrandUpdateView(generics.UpdateAPIView):
    """Admin view to update a brand identified by slug."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

class BrandDeleteView(generics.DestroyAPIView):
    """Admin view to delete a brand identified by slug."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'
