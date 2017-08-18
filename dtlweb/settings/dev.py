from .const import *

# Overwrite any settings variables of base here
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'main/static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'main/media/')

COMPANY_CAREER_EMAIL = 'ynguyen@dytechlab.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3_test'),
    }
}

# Declare variables that are depended on other variables here
TEST_FILES = {
    'DEV': {
        'EN': os.path.join(MEDIA_ROOT, 'developer-en.pdf'),
    },
    'QRES': {
        'EN': os.path.join(MEDIA_ROOT, 'researcher-en.pdf'),
        'CN': os.path.join(MEDIA_ROOT, 'researcher-cn.pdf'),
    },
    'FQRES': {
        'EN': os.path.join(MEDIA_ROOT, 'researcher-en.pdf'),
        'CN': os.path.join(MEDIA_ROOT, 'researcher-cn.pdf'),
    }
}
