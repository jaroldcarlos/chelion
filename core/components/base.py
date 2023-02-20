from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SERVER_DOMAIN = config('SERVER_DOMAIN', default='localhost')

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    ALLOWED_HOSTS = ['*', 'https://3f90-91-117-232-228.eu.ngrok.io']
else:
    ALLOWED_HOSTS = [SERVER_DOMAIN, ]

CSRF_TRUSTED_ORIGINS = [
    'https://siuu.es',
]

INTERNAL_IPS = ['localhost']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

DJANGO_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
THIRDPARTY_APPS = [
    'dynamic_preferences',
    'crispy_forms',
]
LOCAL_APPS = [
    'apps.backend',
    'apps.frontend'
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRDPARTY_APPS

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.UserBasedExceptionMiddleware'
]

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
                'core.context_processors.custom_context'
            ],
            'libraries':{
                'custom_filters': 'core.templatetags.custom_filters',
                'custom_tags': 'core.templatetags.custom_tags',
                'model_tags': 'core.templatetags.models_tags'
            }
        },
    },
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

AUTH_USER_MODEL = 'backend.User'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '..' / 'public_html' / 'static'

MEDIA_URL = '/media/'

if not DEBUG:
    MEDIA_ROOT = BASE_DIR / '..' / 'public_html' / 'media'
else:
    MEDIA_ROOT = BASE_DIR / 'media'


STATICFILES_DIRS = (
    BASE_DIR / 'static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)
