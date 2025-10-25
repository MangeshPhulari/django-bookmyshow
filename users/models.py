# users/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image # <-- 1. Import Pillow

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # --- 2. ADD THIS ENTIRE 'save' METHOD ---
    def save(self, *args, **kwargs):
        """
        Overrides the save method to resize the profile image.
        """
        # Call the original save method
        super().save(*args, **kwargs)

        # Check if an image was uploaded and it's not the default one
        if self.image and self.image.name != 'default.jpg':
            try:
                # Open the image from its path
                img = Image.open(self.image.path)

                # Check if the image is larger than 300x300
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size) # Resizes image, maintaining aspect ratio
                    img.save(self.image.path) # Saves resized image back to the same path
            except (IOError, FileNotFoundError):
                # Handle cases where the file might be missing or corrupt
                pass


# These "signals" automatically create/update a Profile when a User is created/updated
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Check if the profile exists before trying to save it
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # This handles the case for old users who didn't have a profile
        Profile.objects.create(user=instance)