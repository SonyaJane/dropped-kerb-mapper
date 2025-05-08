"""
Django settings for dropped_kerb_mapper project.
"""

from pathlib import Path
import os
import dj_database_url
    
if os.path.isfile('env.py'):
    import env
   
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SECRET_KEY = os.environ.get("SECRET_KEY")

#DEBUG = True if os.environ.get("DEBUG") == 'True' else False
DEBUG = False

ALLOWED_HOSTS = ['www.droppedkerbmapper.com','.herokuapp.com','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_summernote',
    'cloudinary',
    'django_tables2',
    'mapper',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'dropped_kerb_mapper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'dropped_kerb_mapper.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# Override the engine to use GeoDjango's PostGIS backend
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

CSRF_TRUSTED_ORIGINS = [
    "https://*.droppedkerbmapper.com",
    "http://*.droppedkerbmapper.com",
    "https://*.azurewebsites.net",
    "https://*.herokuapp.com",
    "http://127.0.0.1:8000"
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Allauth settings
ACCOUNT_LOGIN_METHODS = {'email'}  # Use email for authentication
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # Required fields for signup
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Require email verification
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True # Log in the user when they click the confirmation link.

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
ACCOUNT_DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
SERVER_EMAIL = DEFAULT_FROM_EMAIL

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

ACCOUNT_FORMS = {
    'signup': 'mapper.forms.CustomSignupForm',
    'login': 'mapper.forms.CustomLoginForm',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model to include mobility device fields
AUTH_USER_MODEL = 'mapper.CustomUser'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}