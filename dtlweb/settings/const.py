"""
Const settings

Specify setting variables that are not depended on other setting variables.
Will be included in setting file of all different environments.
Will be overwrite by setting file of specific environment.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nk)^ano7tw499$)e(@mv*$2-c#cwh#4#17a$nu^s8yrl*tx$r)'

# SECURITY WARNING: don't run with debug turned on in production!
debug = False
ALLOWED_HOSTS = ['localhost',]

INSTALLED_APPS = [
    'recaptcha',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'chinaevent.apps.ChinaeventConfig',
    'recruitment_campaign',
    'bootstrap3',
    'django_crontab',
    'mailer',
    'whitenoise',
    'snowpenguin.django.recaptcha2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


ROOT_URLCONF = 'dtlweb.urls'

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

WSGI_APPLICATION = 'dtlweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

# MAILER settings
# More of usages: https://github.com/pinax/django-mailer/blob/master/docs/usage.rst
MAILER_EMAIL_MAX_BATCH = None
MAILER_EMAIL_MAX_DEFERRED = None
MAILER_EMAIL_THROTTLE = 0  # passed to time.sleep()

COMPANY_CAREER_EMAIL = 'careers@dytechlab.com'


TEST_FILES = {
    'DEV': {
        'EN': os.path.join(MEDIA_ROOT, 'developer-en.pdf'),
    },
    'INTERN_DEVELOPER': {
        'EN': os.path.join(MEDIA_ROOT, 'developer-en.pdf'),
    },
    'QRES': {
        'EN': os.path.join(MEDIA_ROOT, 'researcher-en.pdf'),
        'CN': os.path.join(MEDIA_ROOT, 'researcher-cn.pdf'),
    },
    'FQRES': {
        'EN': os.path.join(MEDIA_ROOT, 'researcher-en.pdf'),
        'CN': os.path.join(MEDIA_ROOT, 'researcher-cn.pdf'),
    },
    'INTERN_FQRES': {
        'EN': os.path.join(MEDIA_ROOT, 'intern-researcher-en.pdf'),
    },
    'INTERN_QRES': {
        'EN': os.path.join(MEDIA_ROOT, 'intern-researcher-en.pdf'),
    },
    'DATA_ENGINEER': {
        'EN': os.path.join(MEDIA_ROOT, 'dtl-project.pdf'),
    },
    'OP_SPECIALIST': {
        'EN': os.path.join(MEDIA_ROOT, 'dtl-project.pdf'),
    },
    'INTERN_DATA_ENGINEER': {
        'EN': os.path.join(MEDIA_ROOT, 'dtl-project.pdf'),
    },
}

FILE_INTERN_EMAILS = os.path.join(MEDIA_ROOT, 'intern-list.csv')


# Crontab settings
CRONJOBS = [
    # cronjob every minute, try to send online tests that are scheduled today
    ('* * * * *', 'main.cron.send_test_token'),
    ('*/5 * * * *', 'main.cron.send_on_remind_tests'),
    # cronjob every minute, try to send mails currently in message queue. if any
    # failure, they will be marked deferred and will not be attempted again by send_mail
    ('* * * * *', 'django.core.management.call_command', ['send_mail'], {'c': 1}),
    # cronjob every 20 min, retry on send_email failure. Deferred mail will be added back
    # to normal queue and attempted again on the next send_mail
    ('0,20,40 * * * *', 'django.core.management.call_command', ['retry_deferred'], {'c': 1}),
    # delete mail log for entries older than 30 days
    ('0 0 * * *', 'django.core.management.call_command', ['purge_mail_log', 30], {'c': 1}),
]

# bootstrap3 settings
BOOTSTRAP3 = {
    'set_placeholder': False,
    'required_css_class': 'bootstrap3-required',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'errorfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['errorfile', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errorfile', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'main': {
            'handlers': ['errorfile', 'console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django_crontab': {
            'handlers': ['errorfile', 'console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
