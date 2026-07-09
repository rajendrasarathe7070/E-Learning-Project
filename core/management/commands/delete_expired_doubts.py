from django.core.management.base import BaseCommand
from core.models import Doubt

class Command(BaseCommand):
    help = 'Delete doubts older than 7 days (unsolved) or 2 days (solved)'

    def handle(self, *args, **options):
        count = 0
        for doubt in Doubt.objects.all():
            if doubt.delete_if_expired():
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} expired doubt(s).'))