from pathlib import Path

import os
import datetime

from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv(".env")

SECRET_KEY = os.environ.get("SECRET_KEY", None)

DEBUG = bool(os.environ.get("DEBUG", None))


# For production
if DEBUG:
    DEBUG = False

# DEBUG = True


ALLOWED_HOSTS = list(str(os.environ.get("ALLOWED_HOSTS")).split(", "))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",  #
    "rest_framework",  #
    "django_filters",  #
    "django_extensions",  #
    "rest_framework_simplejwt.token_blacklist",  #
    "person",  ###
    "patient",  #
    "insurance",  #
    "doctor",  #
    "appointment",  #
    "review",  #
    "specialization",   #
    "geo",   # 
    
    "medical_insurance_firm",  #

    'rest_framework_word_filter',

    'django_seed',  # for seeding the database

    "django.contrib.postgres", # for postgres search
]



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
        "rest_framework.permissions.IsAuthenticated",
    ],
    # "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.JSONRenderer",
    # ],
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),

    'DEFAULT_AUTHENTICATION_BACKENDS': [
        'django.contrib.auth.backends.ModelBackend',
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '10000/day'
    },
}

AUTH_USER_MODEL = "person.Person"



AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "person.authentication.CustomUserAuthBackend",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=45),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  ##

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "project.wsgi.application"

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000/',
    "https://vezeeta-clone-production.up.railway.app",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.environ.get("DATABASE_NAME")),
        "USER": str(os.environ.get("DATABASE_USER")),
        "PASSWORD": str(os.environ.get("DATABASE_PASSWORD")),
        "HOST": str(os.environ.get("DATABASE_HOST")),
        "PORT": int(os.environ.get("DATABASE_PORT")),
        # 'TEST': {
        #     'NAME': '',
        # },
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = True

USE_TZ = True


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"


# Local static files
# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_FILES_DIRS = [BASE_DIR / "static",]


# PRODUCTION STATIC FILES
S3_STATIC_DIR = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{S3_STATIC_DIR}/static/"
STATIC_FILES_STORAGES = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_FILES_DIRS = [BASE_DIR / "static",]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Loacl media files
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# PRODUCTION MEDIA FILES
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "authenticate",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://192.168.0.222:8080",
]

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND_ARGUMENTS = {"fail_silently": False}

# EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# # EMAIL_USE_SSL = bool(os.environ.get('EMAIL_USE_SSL'))
# EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = bool(os.environ.get("EMAIL_USE_TLS"))
# DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

