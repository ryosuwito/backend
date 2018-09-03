from .const import *

# Overwrite any const settings here
DEBUG = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['.dytechlab.com', 'localhost']

ADMINS = [('careers-admin', COMPANY_CAREER_EMAIL)]
SERVER_EMAIL = COMPANY_CAREER_EMAIL

# Declare variables that are depended on other variables here
#
#
