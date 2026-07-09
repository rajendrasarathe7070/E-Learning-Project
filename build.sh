#!/bin/bash
set -o errexit
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Create a superuser if it doesn't exist (optional)
# python manage.py shell < setup_superuser.py
