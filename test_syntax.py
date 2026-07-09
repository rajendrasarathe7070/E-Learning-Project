#!/usr/bin/env python
"""Test script to validate Python syntax of all files."""
import py_compile
import sys
import os

files_to_check = [
    'api/views.py',
    'api/urls.py',
    'core/models.py',
    'core/forms.py',
    'accounts/views_auth.py',
    'accounts/urls.py',
    'minor/settings.py',
    'minor/urls.py',
]

errors = []
for file_path in files_to_check:
    try:
        py_compile.compile(file_path, doraise=True)
        print(f"✓ {file_path}")
    except py_compile.PyCompileError as e:
        errors.append((file_path, str(e)))
        print(f"✗ {file_path}: {e}")

if errors:
    print(f"\n{len(errors)} file(s) with errors")
    sys.exit(1)
else:
    print(f"\nAll {len(files_to_check)} files have valid syntax!")
    sys.exit(0)
