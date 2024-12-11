"""
Django settings for bookednise_pro project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see


https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=i@!9%gg4o^_)-b&o*br1pip8!%-_!8=yqf*1iq(_l(*+y_k$b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    "localhost",
  #  "api.bookednise.com",
    'bookednise.com',
    '192.168.43.121',
    'staging.api.bookednise.com',
    'staging.bookednise.com'
]

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = ''
#EMAIL_PORT = 465
#EMAIL_USE_SSL = True
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#DEFAULT_FROM_EMAIL = ''


#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'etornamasamoah@gmail.com'
#EMAIL_HOST_PASSWORD = 'yrmdporxqxmrvwam'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = 'SwapWing <samahatbarter@gmail.com>'
#BASE_URL = '0.0.0.0:80'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'server269.web-hosting.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # TLS instead of SSL
EMAIL_HOST_USER = 'support@bookednise.com'
EMAIL_HOST_PASSWORD = '19@WeTakingOver@95'
DEFAULT_FROM_EMAIL = 'support@bookednise.com'


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'channels',

    'corsheaders',

    'rest_framework',
    'rest_framework.authtoken',

    'accounts',
    'user_profile',
    'activities',
    'shop',
    'payments',
    'homepage',
    'bookings',
    'admin_app',
    'chats',
    'slots',
    'bank_account'

]

AUTH_USER_MODEL = 'accounts.User'


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bookednise_pro.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookednise_pro.wsgi.application"
ASGI_APPLICATION = "bookednise_pro.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookednise_postgres_staging',
        'USER': 'bookednise_postgres_staging',
        'PASSWORD': 'CwlKJkZNY9nYAN36EbrP9QHrkvGyeUD6JUzn1Lu9lL2DwgqzWTUZWAKDXefLH46h',
        'HOST': 'u0k8cgc480swsgw8wk8c0sow',
        'PORT': 5432,
     }
}

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")  # For static files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Separate media files



HOST_SCHEME = "http://"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


FCM_SERVER_KEY = 'AAAAxOQuav4:APA91bGO5BfxGqVOvfop7ZyrFW1RePVALmhotBv4VMk67KD_IP_9aJfLnBVYQmoJpJw3ho2sKBELLcnMRFhHRl-Ri312kySP7eOLcYJgI0XmyrNZ9CR9fu28bnZn7u5W53dV8Q-4W6oU'


from celery import Celery
app = Celery('bookednise_pro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}






CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    # 'https://api.bookednise.com',
    # 'https://bookednise.com',
    #'https://*.bookednise.com',
    #'http://*.bookednise.com',
    'http://localhost:4040',
    'https://staging.api.bookednise.com',
    'https://staging.bookednise.com'
]



PUSHER_APP_ID = '1875922'
PUSHER_KEY = '88ff191e00149bfda666'
PUSHER_SECRET = '3cb983d4c5b0ff21cb0f'
PUSHER_CLUSTER = 'mt1'
PUSHER_SSL = True


PAYSTACK_SECRET_KEY = 'sk_test_6ff0bf30279f1acafb4ac3e565a0bba4f56c940e'
MNOTIFY_KEY = 'MsxG8Cc6cjRqjJzEZTtjlHBYb'
MNOTIFY_SENDER_ID = 'BookedNise'


GOOGLE_API_KEY = 'AIzaSyCAw7IbX2OgFTlcOiEZ5kTWMPQJ1JeC7mI'


# MinIO Configuration
MINIO_ENDPOINT = "your-minio-endpoint"  # e.g., 'play.min.io'
MINIO_ACCESS_KEY = "your-access-key"
MINIO_SECRET_KEY = "your-secret-key"
MINIO_BUCKET_NAME = "your-bucket-name"
MINIO_USE_SSL = False  # Set to True if your MinIO is set up with SSL (HTTPS)