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

from pathlib import Path
import os
import dj_database_url
from decouple import config
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool) # False in production

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
# Example for Render: ALLOWED_HOSTS = ['your-app-name.onrender.com', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Django staticfiles
    'users',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmyshow.urls'
AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/users/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

# --- Production Database Configuration ---
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL: # Use PostgreSQL in production (Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Optional: persistent connections
            conn_health_checks=True, # Optional
        )
    }
else: # Fallback to SQLite for local development
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
# --- End Database ---

# --- Session Configuration ---
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool) # Should be True in production (HTTPS)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool) # Should be True in production
# --- End Session ---

# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# --- End Email ---

# --- PayU Configuration ---
PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY')
PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT')
PAYU_MODE = config('PAYU_MODE', default='TEST') # Should be 'LIVE' in production if using live keys
# --- End PayU ---

CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files Configuration ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Where Django looks for static files locally
STATIC_ROOT = BASE_DIR / 'staticfiles' # Where collectstatic puts files for production
# --- End Static ---

# --- Media Files Configuration ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # Local storage for development
# IMPORTANT: For Render/production, configure external storage like AWS S3, Cloudinary, etc.
# --- End Media ---

# --- Storage Backend (Whitenoise for Static) ---
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    # Default File Storage (for media) - CHANGE FOR PRODUCTION
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}
# --- End Storage ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'