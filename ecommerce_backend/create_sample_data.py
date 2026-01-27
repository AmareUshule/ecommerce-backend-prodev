import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from categories.models import Category, Brand
from products.models import Product, ProductImage
from users.models import User

print("Creating sample data...")

# Create categories
electronics, _ = Category.objects.get_or_create(
    name='Electronics',
    slug='electronics',
    description='Electronic devices and accessories'
)

clothing, _ = Category.objects.get_or_create(
    name='Clothing',
    slug='clothing',
    description='Fashion and apparel'
)

books, _ = Category.objects.get_or_create(
    name='Books',
    slug='books',
    description='Books and literature'
)

home_garden, _ = Category.objects.get_or_create(
    name='Home & Garden',
    slug='home-garden',
    description='Home improvement and garden supplies'
)

# Create subcategories
smartphones, _ = Category.objects.get_or_create(
    name='Smartphones',
    slug='smartphones',
    parent=electronics,
    description='Mobile phones and smartphones'
)

laptops, _ = Category.objects.get_or_create(
    name='Laptops',
    slug='laptops',
    parent=electronics,
    description='Laptop computers'
)

mens_clothing, _ = Category.objects.get_or_create(
    name="Men's Clothing",
    slug='mens-clothing',
    parent=clothing,
    description="Clothing for men"
)

# Create brands
apple, _ = Brand.objects.get_or_create(
    name='Apple',
    slug='apple',
    description='Technology company'
)

samsung, _ = Brand.objects.get_or_create(
    name='Samsung',
    slug='samsung',
    description='Electronics manufacturer'
)

nike, _ = Brand.objects.get_or_create(
    name='Nike',
    slug='nike',
    description='Sportswear brand'
)

dell, _ = Brand.objects.get_or_create(
    name='Dell',
    slug='dell',
    description='Computer technology company'
)

# Create sample products
iphone, _ = Product.objects.get_or_create(
    name='iPhone 15 Pro',
    slug='iphone-15-pro',
    sku='IPH15PRO-256',
    description='Latest iPhone with A17 Pro chip, 256GB storage',
    price=1099.99,
    discounted_price=999.99,
    category=smartphones,
    brand=apple,
    stock_quantity=50,
    is_featured=True
)

macbook, _ = Product.objects.get_or_create(
    name='MacBook Pro 14"',
    slug='macbook-pro-14',
    sku='MBP14-M3',
    description='14-inch MacBook Pro with M3 chip, 16GB RAM, 512GB SSD',
    price=1999.99,
    category=laptops,
    brand=apple,
    stock_quantity=25,
    is_featured=True
)

galaxy, _ = Product.objects.get_or_create(
    name='Samsung Galaxy S24',
    slug='samsung-galaxy-s24',
    sku='GALS24-256',
    description='Samsung Galaxy S24 with 256GB storage',
    price=899.99,
    category=smartphones,
    brand=samsung,
    stock_quantity=75
)

nike_shoes, _ = Product.objects.get_or_create(
    name='Nike Air Max 270',
    slug='nike-air-max-270',
    sku='NIKE-AM270',
    description='Comfortable running shoes with Air cushioning',
    price=149.99,
    discounted_price=129.99,
    category=mens_clothing,
    brand=nike,
    stock_quantity=100
)

dell_laptop, _ = Product.objects.get_or_create(
    name='Dell XPS 13',
    slug='dell-xps-13',
    sku='DELL-XPS13',
    description='13-inch laptop with Intel Core i7, 16GB RAM, 512GB SSD',
    price=1299.99,
    category=laptops,
    brand=dell,
    stock_quantity=30
)

print("✓ Sample data created successfully!")
print(f"✓ Categories: {Category.objects.count()}")
print(f"✓ Brands: {Brand.objects.count()}")
print(f"✓ Products: {Product.objects.count()}")
