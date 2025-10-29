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
from django.conf import settings

# --- CLOUDINARY IMPORTS ---
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
# -----------------------------

# --- User Authentication Views ---
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
    return redirect('home')

# --- Homepage View ---
def home_view(request):
    print(f"--- [DEBUG Check in View] settings.DEBUG = {settings.DEBUG} ---")
    movies = Movie.objects.all().order_by('-release_date')
    context = {'movies': movies}
    return render(request, 'home.html', context)

# --- Profile View (Corrected Path Saving) ---
# @login_required
# def profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     u_form = UserUpdateForm(instance=request.user)
#     p_form = ProfileUpdateForm(instance=profile)

#     if request.method == 'POST':
#         if 'image' in request.FILES:
#             p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
#             if p_form.is_valid():
#                 image_file = request.FILES['image']
#                 print(f"--- [Profile Save] Found '{image_file.name}'. Attempting direct Cloudinary upload. ---")
#                 try:
#                     image_file.seek(0)
#                     # We still need the folder for the direct upload call
#                     result = cloudinary.uploader.upload(
#                         image_file,
#                         folder="profile_pics", # Explicitly tell Cloudinary the folder
#                         use_filename=True,
#                         unique_filename=False, # Try to keep original name
#                         overwrite=True
#                     )
#                     print("--- [Profile Save] Cloudinary Upload SUCCESS ---")
#                     # Public ID should be "profile_pics/filename_base"
#                     print(f"Public ID returned: {result.get('public_id')}")
#                     print(f"Format returned: {result.get('format')}")
#                     print("---------------------------------------------")

#                     # --- NEW PATH SAVING LOGIC ---
#                     # Extract only the filename (base + extension) from the result
#                     public_id = result.get('public_id') # e.g., "profile_pics/image_name"
#                     file_format = result.get('format')   # e.g., "png"
#                     filename_only = None

#                     if public_id and file_format:
#                         # Get the base filename from the public_id
#                         base_name = os.path.basename(public_id) # Should be "image_name"
#                         # Ensure the extension is present
#                         if not base_name.lower().endswith(f'.{file_format.lower()}'):
#                             filename_only = f"{base_name}.{file_format}" # Add extension
#                         else:
#                             filename_only = base_name # Already includes extension
#                     else:
#                         # Fallback
#                         print(f"--- [Profile Save] CRITICAL WARNING: Missing public_id or format! Using original filename. ---")
#                         filename_only = image_file.name # Use original uploaded filename

#                     # Save ONLY the filename (e.g., "image_name.png") to the database
#                     profile.image.name = filename_only
#                     profile.save(update_fields=['image'])
#                     print(f"--- [Profile Save] Updated profile.image.name to '{profile.image.name}' (filename only) and saved. ---")

#                     return redirect('profile')

#                 except Exception as e:
#                     print("--- [Profile Save] Cloudinary Upload FAILED ---")
#                     print(f"Error: {e}")
#                     messages.error(request, f"Failed to upload profile picture: {e}")
#                     u_form = UserUpdateForm(instance=request.user)
#             else:
#                  u_form = UserUpdateForm(instance=request.user)

#         elif 'username' in request.POST:
#             u_form = UserUpdateForm(request.POST, instance=request.user)
#             if u_form.is_valid():
#                 u_form.save()
#                 return redirect('profile')
#             else:
#                 p_form = ProfileUpdateForm(instance=profile)

#     # --- Booking logic ---
#     user_bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
#     grouped_bookings = {}
#     for booking in user_bookings:
#         if booking.booking_id not in grouped_bookings:
#              grouped_bookings[booking.booking_id] = {
#                  'movie': booking.movie,
#                  'theater': booking.theater,
#                  'booked_at': booking.booked_at,
#                  'seats': []
#              }
#         grouped_bookings[booking.booking_id]['seats'].append(booking.seat.seat_number)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#         'grouped_bookings': grouped_bookings
#     }
#     return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    # Use get_object_or_404 to ensure profile exists or raise 404
    # Note: Using signals should ideally handle creation, but get_or_create is safer.
    profile, created = Profile.objects.get_or_create(user=request.user)
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        if 'image' in request.FILES:
            # We still validate the form, even if we manually upload
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if p_form.is_valid():
                image_file = request.FILES['image']
                print(f"--- [Profile Save] Found '{image_file.name}'. Attempting direct Cloudinary upload. ---")
                try:
                    image_file.seek(0)
                    result = cloudinary.uploader.upload(
                        image_file,
                        folder="profile_pics", # Explicitly tell Cloudinary the folder
                        public_id=os.path.splitext(image_file.name)[0], # Suggest base name
                        overwrite=True
                    )
                    print("--- [Profile Save] Cloudinary Upload SUCCESS ---")
                    print(f"Public ID returned: {result.get('public_id')}")
                    print(f"Format returned: {result.get('format')}")
                    print("---------------------------------------------")

                    # Construct the final correct path
                    public_id = result.get('public_id')
                    file_format = result.get('format')
                    correct_path = None
                    if public_id and file_format:
                        if not public_id.lower().endswith(f'.{file_format.lower()}'):
                            correct_path = f"{public_id}.{file_format}"
                        else:
                            correct_path = public_id
                    else:
                        print(f"--- [Profile Save] CRITICAL WARNING: Missing public_id or format! ---")
                        # Fallback might still be wrong if Cloudinary changed name/format
                        correct_path = os.path.join(Profile._meta.get_field('image').upload_to, image_file.name)

                    # --- MODIFIED SAVE LOGIC ---
                    # Use queryset.update() to bypass model save signals/overrides
                    if correct_path:
                        updated_count = Profile.objects.filter(pk=profile.pk).update(image=correct_path)
                        if updated_count > 0:
                             print(f"--- [Profile Save] Successfully updated profile image path to '{correct_path}' in DB. ---")
                             # Manually update the instance's field in memory for the redirect context (if needed)
                             profile.image.name = correct_path
                        else:
                             print(f"--- [Profile Save] ERROR: Profile object with pk={profile.pk} not found during update! ---")
                             messages.error(request, "Could not update profile picture path.")

                    else:
                         print(f"--- [Profile Save] ERROR: Could not determine correct path to save! ---")
                         messages.error(request, "Could not determine correct image path after upload.")

                    return redirect('profile')

                except Exception as e:
                    print("--- [Profile Save] Cloudinary Upload FAILED ---")
                    print(f"Error: {e}")
                    messages.error(request, f"Failed to upload profile picture: {e}")
                    u_form = UserUpdateForm(instance=request.user)
            else:
                 # If p_form invalid
                 u_form = UserUpdateForm(instance=request.user)

        elif 'username' in request.POST:
             # User details update
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                return redirect('profile')
            else:
                p_form = ProfileUpdateForm(instance=profile)

    # --- Booking logic ---
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
