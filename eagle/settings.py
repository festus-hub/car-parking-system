"""
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

BASE_DIR = Path(__file__).resolve().parent.parent



STATIC_DIR=os.path.join(BASE_DIR,'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sotgn(5f3nd(d=a_5w#((x(u!kio!4!%yh-&&i&w%m@4--t###'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']

ALLOWED_HOSTS = [
    "df0c-41-139-202-31.ngrok-free.app",
    "your-vercel-app-url.vercel.app",
    "localhost",
    "127.0.0.1",
    "testserver"
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classroom',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'rest_framework',
    
]

CSRF_TRUSTED_ORIGINS = [
    "https://df0c-41-139-202-31.ngrok-free.app",
    "https://your-vercel-app-url.vercel.app"  # Add your Vercel domain here
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

ROOT_URLCONF = 'eagle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'eagle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        
    }
}

TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+25416454678"




# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

DATETIME_FORMAT = 'Y-m-d'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'classroom.User'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "static",  
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#LOGIN_URL = 'home_url'
#LOGIN_REDIRECT_URL = 'home'



#LOGIN_URL = 'home'
#LOGIN_REDIRECT_URL = 'home'

STRIPE_PUBLISHABLE_KEY = "your_publishable_key"
STRIPE_SECRET_KEY = "your_secret_key"


MPESA_ENVIRONMENT = "sandbox"
MPESA_CONSUMER_KEY = 'zyf22CG0suhcx2z8mvruUauQ5EsAqTY7DGL91CRjWgrQzBRC'
MPESA_CONSUMER_SECRET = '7SThoERwBcOYmIEnnA5iKBGL5yJ5OspDq2hbEOZaQgkLryX6R91yGPcVt1uLAr7v'
MPESA_SHORTCODE = '174379'
MPESA_EXPRESS_SHORTCODE = '174379'

MPESA_SHORTCODE_TYPE = 'paybill'

MPESA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

MPESA_INITIATOR_USERNAME = 'testapi'

MPESA_CALLBACK_URL = " https://df0c-41-139-202-31.ngrok-free.app"


MPESA_INITIATOR_SECURITY_CREDENTIAL = 'Safaricom999!*!'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'festuskipchirchir15@gmail.com'
EMAIL_HOST_PASSWORD = 'dnue maql srke ushx'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 60


