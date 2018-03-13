from .const import *

# Overwrite any settings variables of base here
DEBUG = True

ALLOWED_HOSTS = ['*']

COMPANY_CAREER_EMAIL = 'ynguyen@dytechlab.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3_dev'),
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
    },
    'INTERN_QRES': {
        'EN': os.path.join(MEDIA_ROOT, 'intern-researcher-en.pdf'),
    },
}

FILE_INTERN_EMAILS = os.path.join(MEDIA_ROOT, 'intern-list.csv')
