#!/usr/bin/env python
"""
Quick script to ensure branches exist in the database.
Run this once after creating/migrating the database.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')
django.setup()

from core.models import Branch

BRANCHES = [
    {'code': 'CSE', 'name': 'Computer Science'},
    {'code': 'ME', 'name': 'Mechanical'},
    {'code': 'CE', 'name': 'Civil'},
    {'code': 'EE', 'name': 'Electrical'},
]

for branch_data in BRANCHES:
    branch, created = Branch.objects.get_or_create(
        code=branch_data['code'],
        defaults={'name': branch_data['name']}
    )
    if created:
        print(f"[+] Created branch: {branch.code} - {branch.name}")
    else:
        print(f"[OK] Branch already exists: {branch.code} - {branch.name}")

print("\n[SUCCESS] All branches are set up!")

