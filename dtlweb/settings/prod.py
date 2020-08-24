from .const import *
from localconfigs import local


# Overwrite any const settings here
DEBUG = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = local.ALLOWED_HOSTS or ['.dytechlab.com', 'localhost', 'ado-pc.dtl']

ADMINS = [('careers-admin', COMPANY_CAREER_EMAIL)]
SERVER_EMAIL = COMPANY_CAREER_EMAIL

SHARE_KEY = local.SHARE_KEY
ONLINE_TEST_HOST = local.ONLINE_TEST_HOST
ACTIVE_USER_URL = local.ACTIVE_USER_URL


def get_online_test_link(token):
    return '/'.join([ONLINE_TEST_HOST, ACTIVE_USER_URL, token])


ONLINE_TEST_ACTIVE_USER_LINK = get_online_test_link


RECAPTCHA_PUBLIC_KEY = local.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = local.RECAPTCHA_PRIVATE_KEY

DATABASES = local.DATABASES

# Declare variables that are depended on other variables here
#
#
