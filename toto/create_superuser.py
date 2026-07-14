import os
import sys
from pathlib import Path

# Ensure project root is on path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toto.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin_test'
email = 'admin@example.com'
password = 'Adm1n!Pass'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created with password '{password}'")
else:
    print(f"User '{username}' already exists")
