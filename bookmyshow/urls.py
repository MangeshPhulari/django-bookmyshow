# bookmyshow/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views # <-- 1. Import your user views

urlpatterns = [
    # --- 2. Set home_view as the homepage ---
    path('', user_views.home_view, name='home'),

    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # Handles /users/register, /users/login etc.
    path('movies/', include('movies.urls')), # Handles /movies/, /movies/movie/1 etc.
]

# Required for media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
