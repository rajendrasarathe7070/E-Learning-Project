import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8^@2q*s@$!b$x#9m%4p1v()r6z7t8y0u')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

SITE_ID = 1

# Security: आपका डोमेन सेट करें (ताकि हर जगह https आए)
DEFAULT_DOMAIN = 'gpclearn.onrender.com'

ALLOWED_HOSTS = [
    '*',
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    'oasis-toolkit-evaluating-consultant.trycloudflare.com',
    'oasis-toolkit-evaluating-consultant.trycloud.com',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'api',
    'accounts',
    'django.contrib.sites', 
    'django.contrib.sitemaps', 
        #sitemeaps 
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

ROOT_URLCONF = 'minor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'minor.wsgi.application'

def get_database_config():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        config = dj_database_url.parse(database_url)
        config.update({
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        })
        return config

<<<<<<< HEAD
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')

    if any([db_name, db_user, db_password, db_host, db_port]):
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name or 'gpc_db',
            'USER': db_user or 'gpc_user',
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port or '5432',
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        }

    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
=======
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'gpc_db'),      # डिफ़ॉल्ट वैल्यू देना है तो दें
        'USER': os.environ.get('DB_USER', 'gpc_user'),      # डिफ़ॉल्ट वैल्यू देना है तो दें
        'PASSWORD': os.environ.get('DB_PASSWORD'),               # ⚠️ बिना डिफ़ॉल्ट के (ENV में डालना अनिवार्य)
        'HOST': os.environ.get('DB_HOST', 'db.khpacdsusjofcdvzzhzs.supabase.co'),          # लोकल के लिए localhost
        'PORT': os.environ.get('DB_PORT', '5432'),
>>>>>>> eef1529a1846656657d1964717b33a4789fe0003
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }


DATABASES = {
    'default': get_database_config(),
}

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for efficient static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom User Model
AUTH_USER_MODEL = 'core.User'

# Login / Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# CSRF & Security for Cloudflare (HTTPS)
CSRF_TRUSTED_ORIGINS = [
    'https://*.trycloudflare.com',
]

# Cookies must be marked Secure when served over HTTPS (Cloudflare).
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Tell Django to trust Cloudflare proxy headers
USE_X_FORWARDED_HOST = False
SECURE_PROXY_SSL_HEADER = ('HTTPS_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


