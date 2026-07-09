#!/usr/bin/env python
"""
Quick Start Guide - Run all necessary setup steps
"""
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("DJANGO PROJECT - QUICK START")
print("=" * 70)

steps = [
    ("Installing dependencies", "pip install -r requirements.txt"),
    ("Running migrations", "python manage.py migrate"),
    ("Collecting static files", "python manage.py collectstatic --noinput"),
    ("Running health check", "python health_check.py"),
]

for step_name, command in steps:
    print(f"\n[*] {step_name}...")
    print(f"    Command: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"\n✗ Failed at step: {step_name}")
        sys.exit(1)
    print(f"✓ {step_name} completed")

print("\n" + "=" * 70)
print("✓ SETUP COMPLETE!")
print("=" * 70)
print("\nTo run the development server:")
print("  python manage.py runserver 0.0.0.0:8000")
print("\nThe server will be available at:")
print("  http://localhost:8000")
print("\nAdmin panel:")
print("  http://localhost:8000/admin")
print("\n" + "=" * 70)
