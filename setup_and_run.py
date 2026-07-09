#!/usr/bin/env python
"""
Install all dependencies and run the server
"""
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("DJANGO PROJECT - SETUP & RUN")
print("=" * 70)

# Step 1: Install requirements
print("\n[1/4] Installing dependencies from requirements.txt...")
print("-" * 70)
result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
if result.returncode != 0:
    print("\n✗ Failed to install dependencies")
    sys.exit(1)
print("✓ Dependencies installed\n")

# Step 2: Run migrations
print("[2/4] Running migrations...")
print("-" * 70)
result = subprocess.run([sys.executable, "manage.py", "migrate"])
if result.returncode != 0:
    print("\n✗ Failed to run migrations")
    sys.exit(1)
print("✓ Migrations completed\n")

# Step 3: Collect static files
print("[3/4] Collecting static files...")
print("-" * 70)
result = subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"])
if result.returncode != 0:
    print("\n✗ Failed to collect static files")
    sys.exit(1)
print("✓ Static files collected\n")

# Step 4: Health check
print("[4/4] Running health check...")
print("-" * 70)
result = subprocess.run([sys.executable, "health_check.py"])
if result.returncode != 0:
    print("\n✗ Health check failed")
    sys.exit(1)
print("✓ Health check passed\n")

print("=" * 70)
print("✓ SETUP COMPLETE!")
print("=" * 70)
print("\nStarting development server...")
print("Server will be available at: http://localhost:8000")
print("Admin panel at: http://localhost:8000/admin")
print("\nPress Ctrl+C to stop the server\n")
print("=" * 70)

# Step 5: Run server
subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
