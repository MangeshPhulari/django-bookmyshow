# users/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# --- ADD THIS MODEL ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Default image assumes 'media/profile_pics/default.jpg'
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Optional: Resize large uploaded images
    # Make sure 'Pillow' is in requirements.txt (pip install Pillow)
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     try:
    #         img = Image.open(self.image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)
    #     except (IOError, FileNotFoundError, ValueError):
    #         # Handle errors gracefully
    #         pass 

# --- ADD THESE SIGNALS ---
# Signal to create a profile when a new user signs up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance) # Use get_or_create for safety

# Signal to save the profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # If profile somehow doesn't exist (e.g., for old users), create it
        Profile.objects.get_or_create(user=instance)