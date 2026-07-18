import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skinovate.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Change 'owner' and 'owner@123' to whatever you prefer
username = "owner"
password = "owner@123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print(f"Superuser {username} already exists.")