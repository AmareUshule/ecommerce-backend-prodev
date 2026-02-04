#!/usr/bin/env bash
python manage.py migrate
gunicorn ecommerce_backend.wsgi:application