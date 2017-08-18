from .const import *

# Overwrite any const settings here
DEBUG = False

ALLOWED_HOSTS = ['localhost', '.dytechlab.com']

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


# Declare variables that are depended on other variables here
#
#
