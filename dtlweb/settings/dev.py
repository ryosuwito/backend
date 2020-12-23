from .const import *
from localconfigs import local

# Overwrite any settings variables of base here
DEBUG = True

ALLOWED_HOSTS = ['ynguyen-pc.dtl', 'localhost', 'ado-pc.dtl']
ALLOWED_HOSTS = local.ALLOWED_HOSTS or ['.dytechlab.com', 'localhost', 'ado-pc.dtl']

COMPANY_CAREER_EMAIL = 'ado@dytechlab.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3_dev'),
    }
}

ADMINS = [('careers-admin', COMPANY_CAREER_EMAIL)]
SERVER_EMAIL = COMPANY_CAREER_EMAIL

SHARE_KEY = local.SHARE_KEY
ONLINE_TEST_HOST = local.ONLINE_TEST_HOST
ACTIVE_USER_URL = local.ACTIVE_USER_URL


def get_online_test_link(token):
    return '/'.join([ONLINE_TEST_HOST, ACTIVE_USER_URL, token])


RECAPTCHA_PUBLIC_KEY = "6LfKRbkUAAAAALE7u26JAF7l1toFWkSFwctDvCW4"
RECAPTCHA_PRIVATE_KEY = "6LfKRbkUAAAAAKIX25s-paiEFxSJxReE_XZoM8iq"


ONLINE_TEST_ACTIVE_USER_LINK = get_online_test_link

DATA_OPERATOR_ATTACHMENTS = local.DATA_OPERATOR_ATTACHMENTS
