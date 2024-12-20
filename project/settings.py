"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import json
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

GOOGLE_SSO_CLIENT_ID = os.getenv('GOOGLE_SSO_CLIENT_ID')
GOOGLE_SSO_PROJECT_ID = os.getenv('GOOGLE_SSO_PROJECT_ID')
GOOGLE_SSO_CLIENT_SECRET = os.getenv('GOOGLE_SSO_CLIENT_SECRET')

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
    'project-1233-6f93642d7963.herokuapp.com',
    '127.0.0.1',
    'localhost',
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

load_dotenv()

# ________________________________________
# connect aiven.io or mysql 
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

# Media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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
        "image": lambda request: static("icons/banner-BdwIal-V.jpg"),
    },
    # "SITE_TITLE": None,
    # "SITE_TITLE": _("Smart lock"),
    # "SITE_HEADER": "Smart lock",

    # "SITE_SYMBOL": "fingerprint",

    "SITE_ICON": {
        "light": lambda request: static("logo/pka.png"),  # light mode
        "dark": lambda request: static("logo/pka.png"),   # dark mode
    },

    "SITE_LOGO": {
        "light": lambda request: static("logo/pka.png"),  # light mode
        "dark": lambda request: static("logo/pka.png"),   # dark mode
    },


    # "TABS": 
    # [
    #     {
    #         "models": [
    #             "auth.user",
    #             # "auth.group",
    #             "authentication.userprofile"
    #         ],
    #         "items": [
    #             {
    #                 "title": _("Users"),
    #                 "icon": "sports_motorsports",
    #                 "link": reverse_lazy("admin:auth_user_changelist"),
    #             },
    #             # {
    #             #     "title": _("Groups"),
    #             #     "icon": "precision_manufacturing",
    #             #     "link": reverse_lazy("admin:auth_group_changelist"),
    #             # },
    #             {
    #                 "title": _("User Profiles"),  # Tên tiêu đề cho UserProfile
    #                 "icon": "person_outline",     # Biểu tượng phù hợp cho UserProfile
    #                 "link": reverse_lazy("admin:authentication_userprofile_changelist"),  # Đường link đến danh sách UserProfile
    #             },
    #         ],
    #     },
    # ],
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
                        "link": reverse_lazy("admin:store_view"),
                    },
                    {
                        "title": _("ChatGPT"),
                        "icon": "forum",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:custom_view"),
                    },
                    # {
                    #     "title": _("Users"),
                    #     "icon": "person",
                    #     "link": reverse_lazy("admin:auth_user_changelist"),
                    # },
                    # {
                    #     "title": _("Groups"),
                    #     "icon": "group",
                    #     "link": reverse_lazy("admin:auth_group_changelist"),
                    # },
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


import firebase_admin
from firebase_admin import credentials, storage 

# cred = credentials.Certificate('smartlock.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'smartlock-ff808.appspot.com'
# })

firebase_config = {
  "type": "service_account",
  "project_id": "smartlock-ff808",
  "private_key_id": "335f9c56d17eed00233622bdbf5797a6f9098566",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCm0oUTl5/mIlLm\nDd8+EvqL2DDIieFzVtjCchxMMiwwfkOMOAzIwA/qKtVkl3v73nRoheAqAlR+NBt1\nBwr/uF5LCxwhO5dllYDGSe1Kb7N5vfK2ayQUBskIqmy32BAtR+v1ld1nmEjn7+ZA\nvy4g/fjQRybPsNwULJrXA7CJk5zQktxZWi5vwjdx/w/J00scgKjZWgZksGf/Xzt9\nNfGMQobu7PvQDH2z6W99V6rhXL3qsIPtwjzV0Q82w11J/nO+DI2wvDiiMpruoG1K\n75Kt2mh4hGxmyZid6UAdwkBIlM8KJ6WckNZ2AreSLF4bis1xET0UmciE09WKht5T\nNBX2VSvjAgMBAAECggEABmXlj7JNgiSH3GXkzXsp28ovWMmc+XD3wEFjH3L/Kd71\n1T9jEiH3mkoJRCHhMfA+s7GKvuG2/t4dvXfHLraR+zvSWN3xuQYqWbCFJskw73bf\nA6sJR7FY7Xmn0Mc7G5l6DcGxK6N2DFsxkAMlEEPdUpOgA/ArCKULTTrJfwVHyuH/\nHkoX4eSooeaWj4TXgyqBHz/URg2HCfGUzDWEeqjGrXLALvp4eQPO0WCHhucmQgeK\noplS3n76he60PjSGIHE2QSfGV+LQ8WmXQm2U5dG/z2aiE5PY+0rMRN5qtkobh763\nRcWUcyJnCU3+yPIhzeFrtbDT5mkPT6H6zLxLjZLMFQKBgQDkTBvRLa8S9Duv3acb\nzpZI2iKiJjBC+qXrU0BpD+xPhCTz1kUpjrPvsO/kU+OiIBKf67SVZmXUGxfH2SJg\njp7JiBeUkZvrBI0Yw5p4uq+xT7F2AvSvzuynYcXCxb22V3Wn6lOCIH3blnZP7dR2\nVuXf+cxlzO/DwS9mZ5GNGCtQFQKBgQC7ELxi3Hmm53YGB21qoZVnGcDV+MDpcGsE\nTpfP3VKrGIt3yJ7MIEqmboPlXoCUAdcDAc2K74LBnC6LhQy5tqauLDR0BrFjqAW3\nOCkEn1RO2YokWpIxDpBF3MNYHHLK5k7jn7fIEJTiH8NJaQxgxtVKjoAFc0yLh1Ax\naxcsp/GSFwKBgQDNsWU+yxJ62WMNyX/PJgtyCFg8EHxbXMoxhQj7oEUiP8WrjNsz\n3kdxJtJ9vrfSU2N0g0JpeaE1wlNi1NiMdvPKULwuOCNrVOZr8ZE0RcAW2d7inTcp\nUB8ZkJZGLzQHHjX73Lzw+aVsO9zNl1NebF0huEfZURSWI3E5qwcRQT2FIQKBgQCr\nDW+l2sMmumnys2H66kwqXaM2RWNpUlGZO6CYA2Jvb19ApeOG9lQsgcv7tgFO1avd\nZQ2laMOg9IafL4dmXj1l8Kf6HJCidubbFfBz+JloDIXEHkmlsBJ+v5KkhEb3f8dN\nXyP3PipV5wN0oikeaVJp/YnU8gxhXdcXiTxEqkE7+wKBgDi37bLZbFUWKARL+EUJ\ndKPujGysPeTa45DG1PjUMdkwxhwAIOQMjWTizvq3gh56A1AmterZyVYcE5wKoadg\nY995MIG0AhuPdvyDwm8GSLDhQJyQAzQMjIFxB6d9LuDD5dI1oYGXjjbuL7GUJRPn\naLpEn2PViknqKRI/AFpJkpFQ\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-x9e32@smartlock-ff808.iam.gserviceaccount.com",
  "client_id": "116672876437269111573",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x9e32%40smartlock-ff808.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'smartlock-ff808.appspot.com'
})










