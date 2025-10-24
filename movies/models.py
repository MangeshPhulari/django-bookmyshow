# # movies/models.py
# import uuid
# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings # Import settings
# from django.core.validators import MinValueValidator, MaxValueValidator
# from urllib.parse import urlparse, parse_qs

# # ==============================================================================
# # UNIFIED MOVIE MODEL
# # ==============================================================================
# class Movie(models.Model):
#     GENRE_CHOICES = [('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Sci-Fi', 'Science Fiction'), ('Thriller', 'Thriller')]
#     LANGUAGE_CHOICES = [('English', 'English'), ('Hindi', 'Hindi'), ('Marathi', 'Marathi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu')]
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     cast = models.TextField(help_text="Comma-separated list of actors")
#     release_date = models.DateField()
#     genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
#     language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
#     youtube_link = models.URLField(blank=True)
#     image = models.ImageField(upload_to='movie_images/')
#     rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def get_youtube_embed_url(self):
#         # ... (method code remains the same) ...
#         if not self.youtube_link: return None
#         try:
#             parsed_url = urlparse(self.youtube_link)
#             if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
#                 if parsed_url.path == '/watch':
#                     video_id = parse_qs(parsed_url.query).get('v');
#                     if video_id: return f"https://www.youtube.com/embed/{video_id[0]}"
#             elif parsed_url.hostname == 'youtu.be':
#                 video_id = parsed_url.path[1:];
#                 if video_id: return f"https://www.youtube.com/embed/{video_id}"
#         except Exception: return None
#         return None

# # ==============================================================================
# # OTHER MODELS
# # ==============================================================================
# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
#     comment = models.TextField()
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self): return f'Review for {self.movie.name} by {self.user.username}'

# class Theater(models.Model):
#     name = models.CharField(max_length=255)
#     movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='theaters')
#     time = models.DateTimeField()
#     price = models.DecimalField(max_digits=7, decimal_places=2, default=150.00)
#     def __str__(self): return f'{self.name} - {self.movie.name} at {self.time.strftime("%d-%b %I:%M %p")}'

# # --- UPDATED Seat MODEL ---
# class Seat(models.Model):
#     STATUS_CHOICES = (
#         ('AVAILABLE', 'Available'),
#         ('RESERVED', 'Reserved'), # Temporarily held
#         ('BOOKED', 'Booked'),     # Permanently booked
#     )
#     theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
#     seat_number = models.CharField(max_length=10)
#     # Replaced 'is_booked' with status and reservation fields
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
#     reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     reserved_until = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f'{self.seat_number} in {self.theater.name} ({self.get_status_display()})'
# # --- END Seat UPDATE ---

# class Booking(models.Model):
#     booking_id = models.CharField(max_length=10, unique=True, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
#     seat = models.ForeignKey(Seat, on_delete=models.CASCADE) # Changed to ForeignKey
#     movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
#     theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
#     booked_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self): return f'Booking by {self.user.username} for {self.seat.seat_number}'

# movies/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from urllib.parse import urlparse, parse_qs
# Removed signal/receiver imports as they are not needed here

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
    youtube_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='movie_images/')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self): return self.name
    def get_youtube_embed_url(self):
        if not self.youtube_link: return None
        try:
            parsed_url = urlparse(self.youtube_link)
            if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
                if parsed_url.path == '/watch': video_id = parse_qs(parsed_url.query).get('v');
                if video_id: return f"https://www.youtube.com/embed/{video_id[0]}"
            elif parsed_url.hostname == 'youtu.be': video_id = parsed_url.path[1:];
            if video_id: return f"https://www.youtube.com/embed/{video_id}"
        except Exception: return None
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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=150.00)
    def __str__(self): return f'{self.name} - {self.movie.name} at {self.time.strftime("%d-%b %I:%M %p")}'

class Seat(models.Model):
    STATUS_CHOICES = (('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('BOOKED', 'Booked'))
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f'{self.seat_number} in {self.theater.name} ({self.get_status_display()})'

class Booking(models.Model):
    booking_id = models.CharField(max_length=50, unique=True, editable=False) # Increased length
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE) # Changed to ForeignKey
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Booking by {self.user.username} for {self.seat.seat_number}'

# --- The duplicate Profile model and signals that were here have been REMOVED ---