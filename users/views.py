# users/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from movies.models import Booking
from .forms import UserRegisterForm, UserUpdateForm
from movies.models import Movie

# ... (register, login_view, logout_view are correct) ...
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
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('movie_list')

# --- ADD THIS VIEW FOR THE HOMEPAGE ---
def home_view(request):
    """ Renders the main home page template and passes all movies. """
    movies = Movie.objects.all().order_by('-release_date') # Get all movies
    context = {
        'movies': movies # Pass movies to the template
    }
    return render(request, 'home.html', context)
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

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
        'grouped_bookings': grouped_bookings
    }
    
    return render(request, 'users/profile.html', context)