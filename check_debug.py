import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourguidepro.settings')
import django
django.setup()
from django.conf import settings
print(f"DEBUG = {settings.DEBUG}")
print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
