#!/usr/bin/env bash
# exit on error
set -o errexit

# install dependencies
pip install -r requirements.txt


echo "Collecting static files..."
python manage.py collectstatic --no-input

# 3. डेटाबेस माइग्रेशन चलाएं (ताकि core_note टेबल वाली एरर ठीक हो सके)
echo "Running database migrations..."
python src/manage.py migrate

echo "Build process completed successfully!"