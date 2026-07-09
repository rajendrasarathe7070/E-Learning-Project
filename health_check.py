#!/usr/bin/env python
"""
Comprehensive test to check Django project health
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')

# Setup Django
django.setup()

from django.core.management import call_command
from io import StringIO

print("=" * 60)
print("DJANGO PROJECT HEALTH CHECK")
print("=" * 60)

# Test 1: Check Django system
print("\n[1] Running Django system check...")
try:
    out = StringIO()
    call_command('check', stdout=out, stderr=out)
    print("✓ Django check passed")
except Exception as e:
    print(f"✗ Django check failed: {e}")
    sys.exit(1)

# Test 2: Import all views
print("\n[2] Importing views...")
try:
    from api import views as api_views
    print("✓ API views imported successfully")
    
    # Check all functions exist
    required_functions = [
        'download_note', 'upload_syllabus', 'notes_list', 'upload_note',
        'delete_note', 'toggle_bookmark', 'my_uploads', 'saved_notes',
        'books_list', 'upload_book', 'upload_pyq', 'syllabus_list',
        'pyqs_list', 'doubts_list', 'ask_doubt', 'reply_to_doubt',
        'mark_best_reply', 'profile_data', 'update_profile'
    ]
    
    for func in required_functions:
        if not hasattr(api_views, func):
            print(f"✗ Missing function: {func}")
            sys.exit(1)
    print(f"✓ All {len(required_functions)} required functions exist")
    
except ImportError as e:
    print(f"✗ Failed to import views: {e}")
    sys.exit(1)

# Test 3: Import models
print("\n[3] Importing models...")
try:
    from core.models import Note, Book, PYQ, Syllabus, Doubt, Reply, Bookmark, Branch, User
    print("✓ All models imported successfully")
except ImportError as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

# Test 4: Import forms
print("\n[4] Importing forms...")
try:
    from core.forms import UserCreationForm
    print("✓ Forms imported successfully")
except ImportError as e:
    print(f"✗ Failed to import forms: {e}")
    sys.exit(1)

# Test 5: Check URLs
print("\n[5] Checking URLs...")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    patterns_count = len(resolver.url_patterns)
    print(f"✓ URL configuration valid ({patterns_count} patterns)")
except Exception as e:
    print(f"✗ URL configuration error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL CHECKS PASSED!")
print("=" * 60)
