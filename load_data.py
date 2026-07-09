#!/usr/bin/env python
"""
Django management command to load data from data.json
Run: python manage.py shell < load_data.py
or: python manage.py loaddata data.json
"""

import os
import json
from pathlib import Path

# Get the project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data.json'

if DATA_FILE.exists():
    print(f"✅ Found {DATA_FILE}")
    print(f"📊 File size: {DATA_FILE.stat().st_size / 1024:.2f} KB")
    print("\n📥 Loading data into database...")
    print("This may take a few moments...\n")
else:
    print(f"❌ File not found: {DATA_FILE}")
    print("\nTo create this file, run:")
    print("  python manage.py dumpdata --all -o data.json")
