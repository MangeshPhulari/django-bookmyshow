# movies/views.py

import shortuuid
from decimal import Decimal
from django.utils import timezone # Import timezone
from datetime import timedelta   # Import timedelta
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.db.models import Avg, Q
from .models import Movie, Theater, Seat, Booking, Review
from .email_utils import send_booking_confirmation_email
from .payu_utils import generate_hash, verify_hash

User = get_user_model()

# --- Helper Function to Release Expired Seats ---
def release_expired_seats():
    """Finds and releases seats whose reservation time has passed."""
    now = timezone.now()
    expired_seats = Seat.objects.filter(status='RESERVED', reserved_until__lt=now)
    expired_count = expired_seats.count()
    if expired_count > 0:
        expired_seats.update(status='AVAILABLE', reserved_by=None, reserved_until=None)
        print(f"Released {expired_count} expired seat reservations.")
# -----------------------------------------------

## MOVIE LISTING AND DETAIL VIEWS (Unchanged)
def movie_list(request):
    # ... (code is correct) ...
    movies = Movie.objects.all().order_by('-release_date'); search_query = request.GET.get('search'); selected_genre = request.GET.get('genre'); selected_language = request.GET.get('language')
    if search_query: movies = movies.filter(Q(name__icontains=search_query) | Q(cast__icontains=search_query))
    if selected_genre: movies = movies.filter(genre=selected_genre)
    if selected_language: movies = movies.filter(language=selected_language)
    context = {'movies': movies, 'genres': Movie.GENRE_CHOICES, 'languages': Movie.LANGUAGE_CHOICES, 'search_query': search_query or '', 'selected_genre': selected_genre, 'selected_language': selected_language}
    return render(request, 'movies/movie_list.html', context)
def movie_detail(request, pk):
    # ... (code is correct) ...
    movie = get_object_or_404(Movie, pk=pk); reviews = movie.reviews.all().order_by('-created_at'); average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if request.method == 'POST' and request.user.is_authenticated: Review.objects.create(user=request.user, movie=movie, comment=request.POST.get('comment'), rating=request.POST.get('rating')); return redirect('movie_detail', pk=pk)
    context = {'movie': movie, 'reviews': reviews, 'average_rating': average_rating, 'theaters': movie.theaters.all()}
    return render(request, 'movies/movie_detail.html', context)
def theater_list(request, movie_id):
    # ... (code is correct) ...
    movie = get_object_or_404(Movie, id=movie_id); theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

## PAYMENT AND BOOKING VIEWS (with Reservation Logic)
def book_seats(request, theater_id):
    # Release expired seats globally first
    release_expired_seats()

    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to book your tickets.")
        login_url = reverse('login'); next_url = request.get_full_path()
        return redirect(f'{login_url}?{REDIRECT_FIELD_NAME}={next_url}')

    theater = get_object_or_404(Theater, id=theater_id)
    # Show seats that are available OR reserved by the current user
    seats = Seat.objects.filter(theater=theater, status__in=['AVAILABLE', 'RESERVED']).exclude(status='RESERVED', reserved_until__lt=timezone.now()).exclude(status='BOOKED')
    # Or, simpler: seats = Seat.objects.filter(theater=theater).exclude(status='BOOKED') and handle display in template

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        if not selected_seat_ids:
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats, 'error': "No seats selected."})

        selected_seats_qs = Seat.objects.filter(id__in=selected_seat_ids, theater=theater)

        # --- Reservation Check ---
        unavailable_seats = []
        seats_to_reserve = []
        now = timezone.now()
        for seat in selected_seats_qs:
            # Check if available OR already reserved by current user within time
            if seat.status == 'AVAILABLE' or (seat.status == 'RESERVED' and seat.reserved_by == request.user and seat.reserved_until > now):
                seats_to_reserve.append(seat)
            else:
                unavailable_seats.append(seat.seat_number)

        if unavailable_seats:
            error_msg = f"Sorry, seat(s) {', '.join(unavailable_seats)} are no longer available. Please select again."
            seats = Seat.objects.filter(theater=theater).exclude(status='BOOKED') # Refresh seat list
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats, 'error': error_msg})
        # --- End Check ---

        # --- Reserve the seats ---
        reservation_duration = timedelta(minutes=5)
        reservation_end_time = now + reservation_duration
        updated_count = Seat.objects.filter(id__in=[s.id for s in seats_to_reserve], status='AVAILABLE').update(
            status='RESERVED', reserved_by=request.user, reserved_until=reservation_end_time
        )
        # Re-fetch the actual IDs of seats now reserved for this user for this action
        successfully_reserved_seat_ids = [str(s.id) for s in Seat.objects.filter(id__in=[s.id for s in seats_to_reserve], reserved_by=request.user, reserved_until=reservation_end_time)]

        if not successfully_reserved_seat_ids:
             messages.error(request, "Could not reserve selected seats. Please try again.")
             return redirect('book_seats', theater_id=theater_id)
        # --- End Reserve ---

        # --- Proceed with PayU ---
        total_amount = Decimal(theater.price) * len(successfully_reserved_seat_ids) # Use actual count reserved
        amount_for_payu = f"{total_amount:.2f}"
        txnid = shortuuid.uuid()
        productinfo = f"Booking for {theater.movie.name}"
        firstname = request.user.first_name or request.user.username
        email = request.user.email
        udf1 = str(request.user.id); udf2 = ",".join(successfully_reserved_seat_ids); udf3 = str(theater_id) # Send ONLY successfully reserved IDs
        payment_hash = generate_hash(txnid, amount_for_payu, productinfo, firstname, email, udf1, udf2, udf3)

        payu_data = {
            'key': settings.PAYU_MERCHANT_KEY, 'txnid': txnid, 'amount': amount_for_payu,
            'productinfo': productinfo, 'firstname': firstname, 'email': email, 'phone': '9999999999',
            'surl': request.build_absolute_uri(reverse('payment_verification')),
            'furl': request.build_absolute_uri(reverse('payment_failure')), 'hash': payment_hash,
            'udf1': udf1, 'udf2': udf2, 'udf3': udf3, 'udf4': '', 'udf5': '',
        }
        return render(request, 'movies/payment_checkout.html', {
            'payu_data': payu_data,
            'reservation_end_time_iso': reservation_end_time.isoformat()
        })

    # GET request: Display seats (template needs to handle statuses)
    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})


@csrf_exempt
def payment_verification(request):
    if request.method == 'POST':
        response_data = request.POST; txnid = response_data.get('txnid')
        udf1 = response_data.get('udf1', ''); udf2 = response_data.get('udf2', ''); udf3 = response_data.get('udf3', ''); udf4 = response_data.get('udf4', ''); udf5 = response_data.get('udf5', '')

        is_hash_verified = verify_hash( response_data.get('status'), txnid, response_data.get('amount'), response_data.get('productinfo'), response_data.get('firstname'), response_data.get('email'), response_data.get('hash'), udf1, udf2, udf3, udf4, udf5)

        if not is_hash_verified or response_data.get('status') != 'success':
            release_seats_on_failure(udf1, udf2, udf3) # Release on failure
            return render(request, 'movies/payment_failure.html', {'error': 'Payment failed or hash mismatch.'})

        try:
            user_id = int(udf1); selected_seat_ids = [int(sid) for sid in udf2.split(',') if sid]; theater_id = int(udf3)
            if not selected_seat_ids: raise ValueError("No seat IDs found")
        except (ValueError, TypeError):
             release_seats_on_failure(udf1, udf2, udf3) # Release on invalid data
             return render(request, 'movies/payment_failure.html', {'error': 'Invalid booking data received.'})

        user = get_object_or_404(User, id=user_id)
        theater = get_object_or_404(Theater, id=theater_id)

        # --- Confirm Reservation and Book ---
        now = timezone.now()
        seats_to_book_qs = Seat.objects.filter(
            id__in=selected_seat_ids,
            status='RESERVED',
            reserved_by=user,
            reserved_until__gt=now # Check reservation validity
        )

        if seats_to_book_qs.count() != len(selected_seat_ids):
            release_seats_on_failure(udf1, udf2, udf3) # Release if reservation expired
            return render(request, 'movies/payment_failure.html', {'error': 'Your seat reservation expired during payment. Please try again.'})

        # Finalize booking: Change status RESERVED -> BOOKED
        booked_seats_info = []
        for seat in seats_to_book_qs:
            Booking.objects.create(booking_id=txnid, user=user, seat=seat, movie=theater.movie, theater=theater)
            seat.status = 'BOOKED'
            seat.reserved_by = None
            seat.reserved_until = None
            seat.save()
            booked_seats_info.append(seat.seat_number)
        # --- End Confirm and Book ---

        if booked_seats_info:
            send_booking_confirmation_email(user, theater, booked_seats_info, txnid)

        login(request, user)
        return redirect('profile')

    return redirect('movie_list')

# --- Helper Function to Release Seats on Failure ---
def release_seats_on_failure(user_id_str, seat_ids_str, theater_id_str):
    """Releases seats reserved by a user if payment fails/cancels."""
    try:
        user_id = int(user_id_str)
        seat_ids = [int(sid) for sid in seat_ids_str.split(',') if sid]
        theater_id = int(theater_id_str)
        # Find user safely
        user = User.objects.filter(id=user_id).first()
        if not user: return # If user not found, can't release by user

        seats_to_release = Seat.objects.filter(
            id__in=seat_ids,
            theater_id=theater_id,
            status='RESERVED',
            reserved_by=user
        )
        released_count = seats_to_release.update(status='AVAILABLE', reserved_by=None, reserved_until=None)
        if released_count > 0:
            print(f"Released {released_count} seats due to payment failure/cancellation for user {user_id}.")
    except (ValueError, TypeError):
        print(f"Error releasing seats: Invalid data received (User: {user_id_str}, Seats: {seat_ids_str}, Theater: {theater_id_str}).")
# ----------------------------------------------------

@csrf_exempt
def payment_failure(request):
    """Handles failed payment callback and releases reserved seats."""
    if request.method == 'POST':
        response_data = request.POST
        udf1 = response_data.get('udf1', ''); udf2 = response_data.get('udf2', ''); udf3 = response_data.get('udf3', '')
        release_seats_on_failure(udf1, udf2, udf3)
    return render(request, 'movies/payment_failure.html')