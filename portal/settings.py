from pathlib import Path
from django.contrib.messages import constants as message_constants
import dj_database_url
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

CSRF_COOKIE_SECURE = True  # Use True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

LOGIN_REDIRECT_URL = 'role'

LOGOUT_REDIRECT_URL = 'home'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'user.backends.EmailBackend',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'compressor',
    'core',
    'user',
    'bot',
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
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'core/templates/core'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context.default_context',
            ],
        },
    },
]


WSGI_APPLICATION = 'portal.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'),  # Fetch the database URL from the .env file
#         conn_max_age=600,                # Optional: Adjust connection persistence
#     )
# }   

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'IIIH College DB',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': config('DATABASE_URL'),  # Fetch the URI from .env
        }  
    }
}

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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATE_INPUT_FORMATS = [
    '%m/%d/%y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m-%d-%Y',
]

# Messaging framework settings
MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# Specify the path for storing compressed files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Enable the COMPRESS_ENABLED setting
COMPRESS_ENABLED = True

# You can also specify additional options, such as compression level
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')

# Attempt to use the first password, and if it fails, use the second
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies
SESSION_COOKIE_SAMESITE = 'Lax'  # Mitigate CSRF risks
CSRF_COOKIE_SAMESITE = 'Lax'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_HSTS_SECONDS = 31536000  # Force HTTPS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}