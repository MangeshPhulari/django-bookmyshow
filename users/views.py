# users/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from movies.models import Booking
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from movies.models import Movie

# ... (register, login_view remain the same) ...
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# --- logout_view (redirects to home) ---
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home') 

# --- (home_view is correct) ---
def home_view(request):
    """ Renders the main home page template and passes all movies. """
    movies = Movie.objects.all().order_by('-release_date') # Get all movies
    context = {
        'movies': movies # Pass movies to the template
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # --- Logic to handle two separate forms ---
    
    if request.method == 'POST':
        # Check if the image form was submitted
        if 'image' in request.FILES:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if p_form.is_valid():
                p_form.save()
                # messages.success(request, 'Profile picture updated!') <-- THIS LINE IS REMOVED
                return redirect('profile')
            else:
                u_form = UserUpdateForm(instance=request.user)
        
        # Check if the details form was submitted
        elif 'username' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                # messages.success(request, 'Account details updated!') <-- THIS LINE IS REMOVED
                return redirect('profile')
            else:
                p_form = ProfileUpdateForm(instance=profile)
        
    if 'u_form' not in locals():
        u_form = UserUpdateForm(instance=request.user)
    if 'p_form' not in locals():
        p_form = ProfileUpdateForm(instance=profile)

    # --- Booking logic (remains the same) ---
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    
    grouped_bookings = {}
    for booking in user_bookings:
        if booking.booking_id not in grouped_bookings:
            grouped_bookings[booking.booking_id] = {
                'movie': booking.movie,
                'theater': booking.theater,
                'booked_at': booking.booked_at,
                'seats': []
            }
        grouped_bookings[booking.booking_id]['seats'].append(booking.seat.seat_number)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'grouped_bookings': grouped_bookings
    }
    
    return render(request, 'users/profile.html', context)