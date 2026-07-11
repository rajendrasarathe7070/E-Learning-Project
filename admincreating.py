import os
import sys
import django

# Django एनवायरनमेंट सेट करें (अपनी settings.py का सही पाथ डालें)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Render के Environment Variables से क्रेडेंशियल्स उठाएं
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not password:
        print("Error: DJANGO_SUPERUSER_PASSWORD environment variable is missing.")
        sys.exit(1)

    # चेक करें कि क्या यह यूजर पहले से डेटाबेस में है
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully!")
    else:
        print(f"Superuser '{username}' already exists. Skipping creation.")

if __name__ == '__main__':
    create_admin()
