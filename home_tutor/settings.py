from pathlib import Path


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = 'django-insecure-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = []


# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [

    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'accounts',
    'tutors',
    'bookings',
    'core',
]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==================================================
# ROOT URL CONFIG
# ==================================================

ROOT_URLCONF = 'home_tutor.urls'


# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [

    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                # Unread notification count
                'bookings.context_processors.unread_notifications',
            ],
        },
    },
]


# ==================================================
# WSGI
# ==================================================

WSGI_APPLICATION = 'home_tutor.wsgi.application'


# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.sqlite3',

        'NAME':
            BASE_DIR / 'db.sqlite3',
    }
}


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==================================================
# LANGUAGE
# ==================================================

LANGUAGE_CODE = 'en-us'


# ==================================================
# TIME ZONE
# ==================================================

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = 'static/'


STATICFILES_DIRS = [

    BASE_DIR / 'static'
]


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==================================================
# LOGIN / LOGOUT SETTINGS
# ==================================================

# IMPORTANT:
# Your actual login page is /login/
LOGIN_URL = '/login/'

# Normal login destination
LOGIN_REDIRECT_URL = '/'

# After logout
LOGOUT_REDIRECT_URL = '/'


# ==================================================
# EMAIL
# ==================================================

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
)


# ==================================================
# MEDIA
# ==================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'