# movies/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # Import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from urllib.parse import urlparse, parse_qs

# ==============================================================================
# UNIFIED MOVIE MODEL
# ==============================================================================
class Movie(models.Model):
    GENRE_CHOICES = [('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Sci-Fi', 'Science Fiction'), ('Thriller', 'Thriller')]
    LANGUAGE_CHOICES = [('English', 'English'), ('Hindi', 'Hindi'), ('Marathi', 'Marathi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu')]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cast = models.TextField(help_text="Comma-separated list of actors")
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
    youtube_link = models.URLField(blank=True) # This is the correct field name
    image = models.ImageField(upload_to='movie_images/')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    # --- THIS FUNCTION HAS BEEN REPLACED ---
    def get_youtube_embed_url(self):
        """
        Converts a standard YouTube 'watch' link into an 'embed' link.
        Uses the 'youtube_link' field.
        """
        if not self.youtube_link:
            return None
        
        video_id = None
        
        try:
            parsed_url = urlparse(self.youtube_link)
            
            # Standard link: https://www.youtube.com/watch?v=VIDEO_ID
            if 'watch' in parsed_url.path:
                query = parse_qs(parsed_url.query)
                if 'v' in query:
                    video_id = query['v'][0]
            
            # Short link: https://youtu.be/VIDEO_ID
            elif 'youtu.be' in parsed_url.netloc:
                video_id = parsed_url.path.lstrip('/')

            if video_id:
                # Handle potential extra parameters (like &t=... or ?t=...)
                video_id = video_id.split('&')[0].split('?')[0]
                return f'https://www.youtube.com/embed/{video_id}'

        except Exception:
            # Failed to parse, return None
            return None
        
        # If no valid format is found, return None
        return None    

    



# ==============================================================================
# OTHER MODELS
# ==============================================================================
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Review for {self.movie.name} by {self.user.username}'

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=150.00)
    def __str__(self): return f'{self.name} - {self.movie.name} at {self.time.strftime("%d-%b %I:%M %p")}'

# --- UPDATED Seat MODEL ---
class Seat(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'), # Temporarily held
        ('BOOKED', 'Booked'),     # Permanently booked
    )
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    # Replaced 'is_booked' with status and reservation fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name} ({self.get_status_display()})'
# --- END Seat UPDATE ---

class Booking(models.Model):
    booking_id = models.CharField(max_length=100, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE) 
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number}'


