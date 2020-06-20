"""
Django settings for recipy project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import pickle
import string

import django_heroku

import nltk

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p0m890w&ke3h#m6iy@fvkyor-0vrcxor(_c@i8c#wc-5dyr#qu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_better_admin_arrayfield',
    'main.apps.MainConfig',
    'crispy_forms',
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

ROOT_URLCONF = 'recipy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'recipy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'df5v9ied8c2kkl',
        'USER': 'ncqloktfuungbd',
        'PASSWORD': 'e43cbb7212cb48b4da2ed45ff43096c9066ccdf514dbd53e4eb8f9ff6ddf1ef3',
        'HOST': 'ec2-54-217-224-85.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    },
]

# JET_DEFAULT_THEME = 'light-gray'
JET_SIDE_MENU_COMPACT = True
# JET_CHANGE_FORM_SIBLING_LINKS = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#
#
# Application specific variables
LEMMATIZER = nltk.WordNetLemmatizer()
LEMMATIZER.lemmatize('load')

try:
    with open('../dataset/stopwords.txt', 'r') as f:
        STOP_WORDS = set(f.read().split())
        CLEANED_STOP_WORDS = set(s.translate(str.maketrans('', '', string.punctuation)) for s in STOP_WORDS)

    with open('../pickles/all_documents.txt', 'rb') as f:
        ALL_DOCUMENTS = pickle.load(f)

    with open('../pickles/index.txt', 'rb') as f:
        INDEX = pickle.load(f)

    with open('../pickles/thesaurus.txt', 'rb') as f:
        STATISTICAL_THESAURUS = pickle.load(f)

except FileNotFoundError:
    with open('dataset/stopwords.txt', 'r') as f:
        STOP_WORDS = set(f.read().split())
        CLEANED_STOP_WORDS = set(s.translate(str.maketrans('', '', string.punctuation)) for s in STOP_WORDS)

    with open('pickles/all_documents.txt', 'rb') as f:
        ALL_DOCUMENTS = pickle.load(f)

    with open('pickles/index.txt', 'rb') as f:
        INDEX = pickle.load(f)

    with open('pickles/thesaurus.txt', 'rb') as f:
        STATISTICAL_THESAURUS = pickle.load(f)

#
#
# Activate Django-Heroku.
django_heroku.settings(locals())
