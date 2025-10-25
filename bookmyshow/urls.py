# bookmyshow/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings               # <-- Import
from django.conf.urls.static import static     # <-- Import
from users import views as user_views

urlpatterns = [
    path('', user_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
]

# --- This block serves media files during development (DEBUG=True) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)