# # movies/email_utils.py

# from decimal import Decimal
# from django.conf import settings
# from django.core.mail import send_mail
# from django.template.loader import render_to_string

# def send_booking_confirmation_email(user, theater, booked_seats_info, booking_id):
#     user_name = user.first_name or user.username
    
#     num_tickets = len(booked_seats_info)
#     ticket_subtotal = theater.price * num_tickets
#     convenience_fee = settings.CONVENIENCE_FEE
#     order_total = ticket_subtotal + convenience_fee

#     context = {
#         'user_name': user_name, 'booking_id': booking_id, 'movie_name': theater.movie.name,
#         'movie_language': theater.movie.language, 'theater_name': theater.name, 'show_time': theater.time,
#         'num_tickets': num_tickets, 'seats': ", ".join(sorted(booked_seats_info)),
#         'ticket_subtotal': ticket_subtotal, 'convenience_fee': convenience_fee, 'order_total': order_total,
#     }

#     html_message = render_to_string('movies/booking_confirmation_email.html', context)
#     subject = f"Booking Confirmed: {theater.movie.name}"

#     try:
#         send_mail(
#             subject=subject, message='', from_email=None,
#             recipient_list=[user.email], html_message=html_message, fail_silently=False,
#         )
#         print(f"Booking confirmation email sent to {user.email} for Booking ID {booking_id}")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# movies/email_utils.py

from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_booking_confirmation_email(user, theater, booked_seats_info, booking_id):
    user_name = user.first_name or user.username
    
    num_tickets = len(booked_seats_info)
    ticket_subtotal = theater.price * num_tickets
    convenience_fee = settings.CONVENIENCE_FEE
    order_total = ticket_subtotal + convenience_fee

    context = {
        'user_name': user_name, 'booking_id': booking_id, 'movie_name': theater.movie.name,
        'movie_language': theater.movie.language, 'theater_name': theater.name, 'show_time': theater.time,
        'num_tickets': num_tickets, 'seats': ", ".join(sorted(booked_seats_info)),
        'ticket_subtotal': ticket_subtotal, 'convenience_fee': convenience_fee, 'order_total': order_total,
    }

    html_message = render_to_string('movies/booking_confirmation_email.html', context)
    subject = f"Booking Confirmed: {theater.movie.name}"

    try:
        send_mail(
            subject=subject,
            message='', # The plain-text message (html_message is used instead)
            # --- THIS IS THE FIX ---
            # Use the verified SendGrid sender address from settings.py
            from_email=settings.SENDGRID_FROM_EMAIL,
            # --------------------
            recipient_list=[user.email], # Sends TO the user who booked
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Booking confirmation email sent to {user.email} for Booking ID {booking_id}")
    except Exception as e:
        # This will now print the full response from SendGrid if it fails
        print(f"Failed to send email, error: {e}")
