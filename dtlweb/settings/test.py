from .const import *

# Overwrite any settings variables of base here
DEBUG = True

ALLOWED_HOSTS = ['ynguyen-pc.dtl', 'localhost']

COMPANY_CAREER_EMAIL = 'ado@dytechlab.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3_test'),
    }
}

ADMINS = [('careers-admin', COMPANY_CAREER_EMAIL)]
SERVER_EMAIL = COMPANY_CAREER_EMAIL
