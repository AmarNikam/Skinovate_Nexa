from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-skinovate-secret-key-change-in-production'
# DEBUG = True     #before whole code
# ================== # after whole code to make it live
DEBUG = False
# ==================
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # added to push it on github # this is added after whole project created
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'skinovate.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'skinovate.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
# STATIC_URL = 'static/'     #before whole code
# ======================== 3 line added after whole code for make it live
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# ========================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ── Email Configuration ───────────────────────────────────────────────────────
# For demo: uses Gmail SMTP. Change to your own credentials in production.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'amarnik88@gmail.com'      # Demo: owner email
EMAIL_HOST_PASSWORD = ''                      # Set your Gmail App Password here
DEFAULT_FROM_EMAIL = 'Skinovate <amarnik88@gmail.com>'

# Owner contact (used as fallback/demo)
OWNER_EMAIL  = 'amarnik88@gmail.com'
OWNER_MOBILE = '7021444055'

# SMS: using Fast2SMS (free tier). Set your API key here.
# Get free key at https://www.fast2sms.com
FAST2SMS_API_KEY = ''   # Set your Fast2SMS API key here
