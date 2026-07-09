#!/usr/bin/env python
"""
Script to migrate data from SQLite3 to PostgreSQL

Usage:
    python migrate_sqlite_to_postgres.py

This script will:
1. Export all data from SQLite3 database
2. Import data into PostgreSQL database
"""

import os
import django
from django.core.management import execute_from_command_line
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')
django.setup()

from django.core.management.commands.dumpdata import Command as DumpCommand
from django.core.management.commands.loaddata import Command as LoadCommand
import json
import sys

def migrate_data():
    """
    Migrate data from SQLite3 to PostgreSQL
    """
    print("\n🔄 Starting data migration from SQLite3 to PostgreSQL...\n")
    
    # Step 1: Export data from current database (SQLite3)
    print("📤 Step 1: Exporting data from SQLite3...")
    try:
        from io import StringIO
        out = StringIO()
        execute_from_command_line(['manage.py', 'dumpdata', '--all', '-o', 'sqlite_backup.json'])
        print("✅ Data exported to sqlite_backup.json\n")
    except Exception as e:
        print(f"❌ Error exporting data: {e}\n")
        return False
    
    # Step 2: Create tables in PostgreSQL
    print("🗄️  Step 2: Creating tables in PostgreSQL...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Tables created in PostgreSQL\n")
    except Exception as e:
        print(f"❌ Error creating tables: {e}\n")
        return False
    
    # Step 3: Import data into PostgreSQL
    print("📥 Step 3: Importing data into PostgreSQL...")
    try:
        execute_from_command_line(['manage.py', 'loaddata', 'sqlite_backup.json'])
        print("✅ Data imported to PostgreSQL\n")
    except Exception as e:
        print(f"❌ Error importing data: {e}\n")
        return False
    
    print("🎉 Migration completed successfully!\n")
    return True

if __name__ == '__main__':
    success = migrate_data()
    sys.exit(0 if success else 1)
