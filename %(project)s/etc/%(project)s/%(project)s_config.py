from os.path import join, dirname

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = False

SESSION_COOKIE_DOMAIN = None

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = '%(project)s'
DATABASE_USER = '%(project)s'

MEDIA_ROOT = '%(path)s/repo/%(project)s/media'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

