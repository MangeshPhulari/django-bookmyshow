# users/management/commands/createsu.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config # Or use os.environ
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exist, using environment variables for credentials.'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists. Skipping creation.'))
            return

        # Get credentials securely from environment variables
        # Use os.environ directly as decouple might not be fully configured at this stage
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stderr.write(self.style.ERROR(
                'Missing ADMIN_USERNAME, ADMIN_EMAIL, or ADMIN_PASSWORD environment variables.'
            ))
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))