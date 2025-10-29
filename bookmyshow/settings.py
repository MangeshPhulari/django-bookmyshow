# # bookmyshow/settings.py

# from pathlib import Path
# import os
# import dj_database_url
# from decouple import config
# from decimal import Decimal

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # --- 1. SECRET KEY ---
# SECRET_KEY = config('SECRET_KEY', default='django-insecure-a-safe-default-key-for-local-dev')

# # --- 2. DEBUG ---
# DEBUG = config('DEBUG', default=True, cast=bool)

# # --- 3. ALLOWED_HOSTS ---
# ALLOWED_HOSTS = ['127.0.0.1']
# RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# # --- APPLICATION DEFINITION ---
# # This order is now correct to prevent conflicts.
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
    
#     'whitenoise.runserver_nostatic',  # <-- Must be before staticfiles
#     'django.contrib.staticfiles',     # <-- Handles static files
    
#     'cloudinary_storage',             # <-- Handles media files
#     'cloudinary',
    
#     'users',
#     'movies',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'bookmyshow.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
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

# # --- 4. DATABASES ---
# DATABASES = {
#     'default': dj_database_url.config(
#         default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
#         conn_max_age=600
#     )
# }

# # --- 5. PAYU / EMAIL ---
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_USER', default=None)
# EMAIL_HOST_PASSWORD = config('EMAIL_PASS', default=None)
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY', default=None)
# PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT', default=None)
# PAYU_MODE = 'TEST'
# CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))

# # --- 6. CLOUDINARY CONFIGURATION ---
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=None),
#     'API_KEY': config('CLOUDINARY_API_KEY', default=None),
#     'API_SECRET': config('CLOUDINARY_API_SECRET', default=None),
# }


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


# # --- 7. STATIC FILES (WHITENOISE) ---
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles' 
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# # --- 8. MEDIA FILES (Smart Switching) ---
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# if DEBUG:
#     # --- Development Settings ---
#     DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# else:
#     # --- Production (Render) Settings ---
#     DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# # --- 9. OTHER SETTINGS ---
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# LOGIN_URL = '/users/login/'
# AUTH_USER_MODEL = 'auth.User'


# bookmyshow/settings.py

from pathlib import Path
import os
import dj_database_url
from decouple import config # Uses python-decouple
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Settings ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-a-safe-default-key-for-local-dev')
DEBUG = config('DEBUG', default=True, cast=bool) # Reads False on Render

ALLOWED_HOSTS = ['127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'users',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmyshow.urls'

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

# --- Databases ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- Email Configuration (Using SendGrid) ---
# Set the backend
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
# Read API Key from environment (CRITICAL)
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default=None)
# Set your desired "From" email address (must be verified in SendGrid or use a verified domain)
SENDGRID_FROM_EMAIL = config('SENDGRID_FROM_EMAIL', default='no-reply@yourdomain.com') # CHANGE THIS or verify sender in SendGrid
# Optional: Suppress exceptions during sending (False recommended for debugging)
# SENDGRID_RAISE_EXCEPTIONS = False

# --- PayU Configuration ---
PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY', default=None)
PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT', default=None)
PAYU_MODE = 'TEST' # Keep as TEST unless you have live keys
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))

# --- Cloudinary Configuration ---
# Uses CLOUDINARY_URL environment variable primarily
CLOUDINARY_STORAGE = {
     # You might still need Cloud Name here for some template tags, even if using URL
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=None),
    'API_KEY': config('CLOUDINARY_API_KEY', default=None), # Optional if using URL
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=None), # Optional if using URL
}

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

# --- Static Files (Whitenoise) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Smart Switching based on DEBUG) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if DEBUG:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- Other Settings ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/users/login/'
AUTH_USER_MODEL = 'auth.User' # Using default Django user model
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))