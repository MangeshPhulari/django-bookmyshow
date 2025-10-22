# movies/admin.py

from django.contrib import admin
from .models import Movie, Review, Theater, Seat, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'language', 'rating', 'release_date')
    list_filter = ('genre', 'language', 'release_date')
    search_fields = ('name', 'cast')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    # Added 'price' to display
    list_display = ('name', 'movie', 'time', 'price')
    list_filter = ('movie',) # Filter by movie
    search_fields = ('name', 'movie__name') # Search by theater name or movie name

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    # Updated list_display to use new status fields
    list_display = ('theater', 'seat_number', 'status', 'reserved_by', 'reserved_until')
    # Added filters for status and theater
    list_filter = ('status', 'theater__name')
    search_fields = ('seat_number', 'theater__name', 'reserved_by__username')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Added booking_id to display
    list_display = ('booking_id', 'user', 'seat', 'movie', 'theater', 'booked_at')
    list_filter = ('booked_at', 'theater__name', 'movie__name', 'user__username')
    search_fields = ('booking_id', 'user__username', 'seat__seat_number', 'movie__name')
    # Make relationship fields clickable links in admin
    raw_id_fields = ('user', 'seat', 'movie', 'theater')

# Register Review model if it's not already using the decorator
# Check if Review is already registered to avoid errors
if not admin.site.is_registered(Review):
    admin.site.register(Review)