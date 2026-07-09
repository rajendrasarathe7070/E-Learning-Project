import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minor.settings')
django.setup()

from django.core.management import call_command
from io import StringIO

# Export data with UTF-8 encoding
out = StringIO()
try:
    call_command('dumpdata', 'core', 'accounts', stdout=out, indent=2)
    data = out.getvalue()

    # Write with UTF-8 encoding
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(data)

    print("✅ Data exported successfully to data.json")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative method...")

    # Alternative: Export without some problematic data
    try:
        call_command('dumpdata', 'core', '--exclude', 'core.user', stdout=out, indent=2)
        data = out.getvalue()
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(data)
        print("✅ Partial data exported (without users)")
    except Exception as e2:
        print(f"❌ Also failed: {e2}")