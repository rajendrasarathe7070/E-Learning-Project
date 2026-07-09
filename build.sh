#!/usr/bin/env bash
# exit on error
set -o errexit

# install dependencies
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

python manage.py makemigrations
# migrate database
python manage.py migrate