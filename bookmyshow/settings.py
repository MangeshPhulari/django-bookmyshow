# # bookmyshow/settings.py

# from pathlib import Path
# import os
# import dj_database_url
# from decouple import config
# from decimal import Decimal # Make sure Decimal is imported if used here

# BASE_DIR = Path(__file__).resolve().parent.parent
# SECRET_KEY = config('SECRET_KEY')
# DEBUG = True
# ALLOWED_HOSTS = ["*"]

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions', # Ensure sessions app is installed
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'users',
#     'movies',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware', # <<< MUST BE HERE
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware', # <<< MUST BE AFTER SESSION
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'bookmyshow.urls'
# AUTH_USER_MODEL = 'auth.User'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# LOGIN_URL = '/users/login/'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'], # Use BASE_DIR for consistency
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'bookmyshow.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # --- SESSION CONFIGURATION ---
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# # Try setting SameSite to None for development
# SESSION_COOKIE_SAMESITE = None
# # Secure must be False for http://127.0.0.1
# SESSION_COOKIE_SECURE = False
# # -----------------------------

# # EMAIL CONFIGURATION
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_PASS')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # PAYU CONFIGURATION
# PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY')
# PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT')
# PAYU_MODE = 'TEST'

# # CONVENIENCE FEE
# CONVENIENCE_FEE = Decimal('30.68') # Make sure Decimal is imported

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static'] # Tell Django where your project-wide static files are

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CONVENIENCE_FEE = Decimal('30.68')

# bookmyshow/settings.py

# bookmyshow/settings.py

# bookmyshow/settings.py

from pathlib import Path
import os
import dj_database_url
from decouple import config
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Security Settings ---
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool) # Default to False for safety
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
# Example for Render: ALLOWED_HOSTS='your-app-name.onrender.com,127.0.0.1' in Render Env Vars

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage', # For Cloudinary Media Files
    'django.contrib.staticfiles', # Must be AFTER cloudinary_storage
    'cloudinary', # Cloudinary app itself
    'users', # Your user app
    'movies', # Your movie app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise for static files - Place high
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmyshow.urls'
AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/users/login/' # Your app's login URL

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Project-level templates (home.html)
        'APP_DIRS': True, # Allow app templates (users/, movies/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmyshow.wsgi.application'

# --- Database Configuration (Render PostgreSQL / Local SQLite) ---
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)}
else: # Fallback for local dev
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# --- Session Configuration ---
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG # True in production (HTTPS)
CSRF_COOKIE_SECURE = not DEBUG # True in production (HTTPS)

# --- Email Configuration (Example: Gmail) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER') # From .env or Render Env Vars
EMAIL_HOST_PASSWORD = config('EMAIL_PASS') # From .env or Render Env Vars
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- PayU Configuration ---
PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY') # From .env or Render Env Vars
PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT') # From .env or Render Env Vars
PAYU_MODE = config('PAYU_MODE', default='TEST') # 'TEST' or 'LIVE'

# --- Custom App Settings ---
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files (Managed by Whitenoise) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Where Django looks locally
STATIC_ROOT = BASE_DIR / 'staticfiles' # Target for collectstatic

# --- Media Files (Managed by Cloudinary) ---
MEDIA_URL = '/media/' # Base URL path for media files on Cloudinary
# MEDIA_ROOT is not needed when using Cloudinary as default storage
# MEDIA_ROOT = BASE_DIR / 'media'

# --- Cloudinary Configuration ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'), # From .env or Render Env Vars
    'API_KEY': config('CLOUDINARY_API_KEY'),       # From .env or Render Env Vars
    'API_SECRET': config('CLOUDINARY_API_SECRET'), # From .env or Render Env Vars
    'SECURE': True, # Use HTTPS URLs
}

# --- Storage Backends ---
STORAGES = {
    # Default backend for handling MEDIA files (user uploads)
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # Backend for handling STATIC files (CSS, JS, project images)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# --- End Storage Backends ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Production Security Settings (Uncomment and configure as needed) ---
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # If behind a proxy like Render's
# SECURE_SSL_REDIRECT = not DEBUG # Redirect HTTP to HTTPS
# SECURE_HSTS_SECONDS = 31536000 # Example: 1 year. Enable HSTS
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_SECURE = not DEBUG # Already set above
# SESSION_COOKIE_SECURE = not DEBUG # Already set above
# X_FRAME_OPTIONS = 'DENY'