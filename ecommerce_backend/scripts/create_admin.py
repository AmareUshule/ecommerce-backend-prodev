"""Utility script to create a default superuser for local development.

This script ensures the project root is on `sys.path`, sets up Django
and creates a superuser with configured credentials if one does not
already exist. Intended for development convenience only.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

email = 'admin@example.com'
username = 'admin'
password = 'adminpass'

if User.objects.filter(email=email).exists():
    print('Superuser already exists:', email)
else:
    User.objects.create_superuser(email=email, username=username, password=password)
    print('Created superuser:', email)
