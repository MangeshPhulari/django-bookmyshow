# bookmyshow/settings.py

from pathlib import Path
import os
import dj_database_url  # <-- This is crucial
from decouple import config
from decimal import Decimal

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. SECRET KEY ---
# Reads from Render's environment
SECRET_KEY = config('SECRET_KEY', default='django-insecure-a-safe-default-key-for-local-dev')

# --- 2. DEBUG ---
# Reads 'False' from Render's environment
DEBUG = config('DEBUG', default=True, cast=bool)

# --- 3. ALLOWED_HOSTS ---
# Automatically adds your Render domain
ALLOWED_HOSTS = ['127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # <-- Added for static files
    'django.contrib.staticfiles',
    'users',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Added for static files
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

# --- 4. DATABASES ---
# Reads from Render's 'DATABASE_URL' environment variable
DATABASES = {
    'default': dj_database_url.config(
        # Default to your local sqlite db for development
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- 5. PAYU / EMAIL ---
# Reads all these from Render's environment
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_PASS', default=None)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY', default=None)
PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT', default=None)
PAYU_MODE = 'TEST'
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- 6. STATIC FILES (WHITENOISE) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# This is the folder Whitenoise will collect all static files into
STATIC_ROOT = BASE_DIR / 'staticfiles' 
# This tells Whitenoise to handle compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- 7. MEDIA FILES ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- 8. OTHER SETTINGS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/users/login/'
AUTH_USER_MODEL = 'auth.User'
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))