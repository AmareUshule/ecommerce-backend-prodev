"""Views for product API endpoints.

This module provides class-based views for listing, retrieving and
managing `Product` objects and creating product reviews. Views are
implemented using Django REST Framework generic views and expose
filtering/search/ordering hooks used by the public API.
"""
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product, ProductReview
from .serializers import ProductSerializer, ProductListSerializer, ProductReviewSerializer

class ProductListView(generics.ListAPIView):
    """List view returning lightweight product representations.

    Supports filtering by category/brand, price range, search and
    ordering. Uses `ProductListSerializer` for compact responses.
    """
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Allow filtering by category id or slug (via 'category' param), brand id, and featured flag
    filterset_fields = ['category', 'category__slug', 'brand', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images')
        # Use select_related for FK lookups (single row joins) and
        # prefetch_related for related sets (`images`) to minimize queries.

        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        # Category filter can be provided as id or slug via ?category=123 or ?category=slug
        category_param = self.request.query_params.get('category')
        if category_param:
            # If the `category` value looks numeric treat it as an id,
            # otherwise treat it as a slug. This keeps the public API
            # flexible for clients that prefer either form.
            if category_param.isdigit():
                queryset = queryset.filter(category__id=category_param)
            else:
                queryset = queryset.filter(category__slug=category_param)
        
        if min_price:
            # Apply minimum price (inclusive) if provided.
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            # Apply maximum price (inclusive) if provided.
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a single active product by `slug`."""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductCreateView(generics.CreateAPIView):
    """Admin-only view to create new `Product` instances."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductUpdateView(generics.UpdateAPIView):
    """Admin-only view to update products identified by `slug`."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

class ProductDeleteView(generics.DestroyAPIView):
    """Admin-only view to delete products identified by `slug`."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

class ProductReviewCreateView(generics.CreateAPIView):
    """Authenticated endpoint to create `ProductReview` for a product.

    The product is determined from the URL `slug` and the authenticated
    user is attached as the review author in `perform_create`.
    """
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Attach the `Product` (from URL `slug`) and the current user.

        If the slug does not resolve to a product, `product` will be
        `None` and the serializer is expected to validate that case.
        """
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug).first()
        serializer.save(user=self.request.user, product=product)
