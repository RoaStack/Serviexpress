import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("SUPERUSER_USERNAME")
password = os.getenv("SUPERUSER_PASSWORD")
email = os.getenv("SUPERUSER_EMAIL")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"✅ Superuser '{username}' created.")
else:
    print(f"ℹ️ Superuser '{username}' already exists. Skipping.")
