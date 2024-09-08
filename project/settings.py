"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from . info import *
from decouple import Config


# setting.py


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ________________________________________
# send mail
# ________________________________________
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT


# settings.py

# ________________________________________
# google sso
# ________________________________________
GOOGLE_SSO_CLIENT_ID = "740073010366-mrsboulhnt2b77o9r9i591r5n5snd9ie.apps.googleusercontent.com"
GOOGLE_SSO_PROJECT_ID = "flower-shop-428110"
GOOGLE_SSO_CLIENT_SECRET = "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"

# ________________________________________
# send mail
# ________________________________________
GOOGLE_SSO_ALLOWABLE_DOMAINS = ["gmail.com"]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f7bv8qrx=j^kl(tvvjo5+g&a)+8ut^j@wbc4m+!kswr=(68_^-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'project-1233-6f93642d7963.herokuapp.com'
    ]
# ALLOWED_HOSTS = ['*']

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    "unfold",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authentication',

    "django_google_sso",  

    "unfold.contrib.filters",
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# load_dotenv()

# ________________________________________
# connect aiven.io
# ________________________________________
DATABASES = {
    "default": {
        "ENGINE": os.getenv('DB_ENGINE'),
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}   

# ________________________________________
# connect xampp v3.3.0 mysql
# ________________________________________

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'parking',
#         'USER': 'root',
#         'PASSWORD': 'ducanh12',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# ________________________________________
# connect sqlite3
# ________________________________________

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Add these settings if you have static files outside of app directories
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Directory where collectstatic will collect static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# ________________________________________
# connect heroku
# ________________________________________
import django_heroku
django_heroku.settings(locals())


# ________________________________________
# theme django unfold
# ________________________________________
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "DASHBOARD_CALLBACK": "project.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("icons/illustration.jpg"),
    },
    # "SITE_TITLE": None,
    "SITE_TITLE": _("Smart car park"),
    "SITE_HEADER": "Smart car park",
    # "SITE_SYMBOL": "directions_car",
    "SITE_SYMBOL": "fingerprint",
    # "SITE_SYMBOL": "icons/icon.svg",
    "TABS": 
    [
        {
            "models": [
                "auth.user",
                "auth.group"
            ],
            "items": [
                {
                    "title": _("Users"),
                    "icon": "sports_motorsports",
                    "link": reverse_lazy("admin:auth_user_changelist"),
                },
                {
                    "title": _("Groups"),
                    "icon": "precision_manufacturing",
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Store"),
                        "icon": "storefront",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "project.utils.badge_callback",
                    },
                    {
                        "title": _("Statistical"),
                        "icon": "bar_chart",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Standings"),
                        "icon": "star",
                        "link": reverse_lazy("admin:index"),
                    }, 
                ],
            },
            {
                "title": _("Users & Groups"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            # {
            #     "separator": True,
            #     "items": [
            #         {
            #             "title": _("Users"),
            #             "icon": "person",
            #             "link": reverse_lazy("admin:auth_user_changelist"),
            #             "badge": "project.utils.badge_callback",
            #         },
            #         {
            #             "title": _("Groups"),
            #             "icon": "people",
            #             "link": reverse_lazy("admin:auth_group_changelist"),
            #         }, 
            #         {
            #             "title": _("Tasks"),
            #             "icon": "task_alt",
            #             "link": reverse_lazy(
            #                 "admin:auth_group_changelist"
            #             ),
            #         },
            #     ],
            # },
        ],
    },
}


# https://github.com/topics/responsive

DEFAULT_CONTENT_TYPE = 'text/html'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'anhnguyen2k373@gmail.com'
EMAIL_HOST_PASSWORD = 'apjahlrpflvncpfy'





