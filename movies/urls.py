# movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/theaters/', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/', views.book_seats, name='book_seats'),
    
    # --- FINAL PAYMENT URLS ---
    path('payment/verify/', views.payment_verification, name='payment_verification'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
]