import os
import django
import json
import sys

# Ensure project root is on path (so `ecommerce_backend` package can be imported)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from categories.models import Category, Brand
from products.models import Product

User = get_user_model()
client = APIClient()

print('Starting smoke tests...')

# Ensure sample data
cat, _ = Category.objects.get_or_create(name='TestCat', slug='testcat')
brand, _ = Brand.objects.get_or_create(name='TestBrand', slug='testbrand')
prod, _ = Product.objects.get_or_create(
    name='Test Product',
    slug='test-product',
    sku='TESTSKU123',
    description='Sample product for smoke tests',
    price=9.99,
    category=cat,
    brand=brand,
)

# Create normal user
email = 'smoke@example.com'
password = 'smokepass123'
if not User.objects.filter(email=email).exists():
    User.objects.create_user(email=email, username='smokeuser', password=password)
    print('Created user', email)
else:
    print('User exists', email)

# Product list (public)
resp = client.get('/api/products/')
print('GET /api/products/ ->', resp.status_code)
try:
    data = resp.json()
    print('Products returned:', data.get('results', data) if isinstance(data, dict) else data)
except Exception:
    print('Could not parse product list response')

# Login to get tokens
login_resp = client.post('/api/users/login/', {'email': email, 'password': password}, format='json')
print('POST /api/users/login/ ->', login_resp.status_code)
try:
    lr = login_resp.json()
    access = lr.get('access')
    refresh = lr.get('refresh')
    print('Login response keys:', list(lr.keys()))
except Exception:
    print('Login failed, response:', login_resp.content)
    access = None

# Create review if logged in
if access:
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    review_resp = client.post(f'/api/products/{prod.slug}/reviews/', {'rating':5, 'title':'Great', 'comment':'Nice.'}, format='json')
    print(f'POST /api/products/{prod.slug}/reviews/ ->', review_resp.status_code)
    try:
        print('Review response:', review_resp.json())
    except Exception:
        print('Review response content:', review_resp.content)
else:
    print('Skipping review test; no access token')

# Create superuser and test admin product create
admin_email = 'admin@example.com'
admin_pass = 'adminpass123'
if not User.objects.filter(email=admin_email).exists():
    User.objects.create_superuser(email=admin_email, username='admin', password=admin_pass)
    print('Created superuser', admin_email)

admin_login = client.post('/api/users/login/', {'email': admin_email, 'password': admin_pass}, format='json')
print('Admin login status:', admin_login.status_code)
try:
    aj = admin_login.json()
    admin_access = aj.get('access')
except Exception:
    admin_access = None

if admin_access:
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_access}')
    new_prod_data = {
        'name': 'Admin Created',
        'slug': 'admin-created',
        'sku': 'ADMIN123',
        'description': 'Created by admin via API',
        'price': '19.99',
        'category_id': cat.id,
        'brand_id': brand.id,
        'stock_quantity': 10,
    }
    create_resp = client.post('/api/products/create/', new_prod_data, format='json')
    print('POST /api/products/create/ ->', create_resp.status_code)
    try:
        print('Create product response:', create_resp.json())
    except Exception:
        print('Create response content:', create_resp.content)
else:
    print('Admin login failed; skipping admin product create')

print('Smoke tests completed.')
