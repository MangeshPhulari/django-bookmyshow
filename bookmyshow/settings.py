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
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # --- CHANGE: Moved staticfiles before cloudinary_storage ---
    'django.contrib.staticfiles',
    'cloudinary_storage', # For Cloudinary Media Files
    'cloudinary', # Cloudinary app itself
    'users',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise
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

# --- Database Configuration ---
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)}
else: # Fallback for local dev
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# --- Session Configuration ---
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'; EMAIL_HOST = 'smtp.gmail.com'; EMAIL_PORT = 587; EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER'); EMAIL_HOST_PASSWORD = config('EMAIL_PASS'); DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- PayU Configuration ---
PAYU_MERCHANT_KEY = config('PAYU_MERCHANT_KEY'); PAYU_MERCHANT_SALT = config('PAYU_MERCHANT_SALT'); PAYU_MODE = config('PAYU_MODE', default='TEST')

# --- Custom App Settings ---
CONVENIENCE_FEE = Decimal(config('CONVENIENCE_FEE', default='30.68'))

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [ {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}, ]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'; TIME_ZONE = 'UTC'; USE_I18N = True; USE_TZ = True

# --- Static Files (Managed by Whitenoise) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- Media Files (Managed by Cloudinary) ---
MEDIA_URL = '/media/'
# MEDIA_ROOT is NOT used by Cloudinary storage

# --- Cloudinary Configuration ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    # --- ADD THIS FLAG ---
    # Explicitly tell dj3-cloudinary-storage NOT to manage static files
    'MANAGE_STATICFILES': False,
    # Remove these if MANAGE_STATICFILES works
    # 'STATICFILES_MANIFEST_ROOT': STATIC_ROOT,
    # 'STATIC_IMAGES_EXTENSIONS': [],
    # 'STATIC_VIDEOS_EXTENSIONS': [],
}

# --- Storage Backends ---
STORAGES = {
    # Default backend for handling MEDIA files -> Cloudinary
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # Backend for handling STATIC files -> Whitenoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Production Security (Review/Uncomment as needed) ---
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# ... other security settings ...