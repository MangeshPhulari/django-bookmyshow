# users/migrations/0002_create_superuser.py (or whatever yours is named)

from django.db import migrations
import os  # Import os to read environment variables

def create_superuser(apps, schema_editor):
    """
    Creates a superuser from environment variables.
    """
    User = apps.get_model('auth', 'User')

    # Get credentials from environment variables
    username = os.environ.get('ADMIN_USER')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASS')

    # Don't do anything if the variables aren't set
    if not username or not email or not password:
        print("Superuser environment variables not set. Skipping superuser creation.")
        return

    # Don't create if a user with that name already exists
    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists. Skipping.")
        return

    # Create the superuser
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully!")
    except Exception as e:
        print(f"Error creating superuser: {e}")


class Migration(migrations.Migration):

    # This depends on the migration that created your 'Profile' model.
    # If your first migration was named 0001_initial.py, this is correct.
    dependencies = [
        ('users', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]