# -*- coding: utf-8 -*-
from biostar.settings.base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

START_CATEGORIES = [
    u"Últimos", "Abiertos",
]

NAVBAR_TAGS = []

END_CATEGORIES = []

POST_TAG_LIST = NAVBAR_TAGS

CATEGORIES = START_CATEGORIES + NAVBAR_TAGS + END_CATEGORIES

TOP_BANNER = ""


__DEFAULT_BIOSTAR_ADMIN_NAME = "Admin"
__DEFAULT_BIOSTAR_ADMIN_EMAIL = "admin@site.me"
__DEFAULT_SECRET_KEY = 'admin@site.me'
__DEFAULT_SITE_DOMAIN = 'www.site.me'
__DEFAULT_FROM_EMAIL = 'noreply@site.me'

SITE_NAME = "SITE"

EMAIL_REPLY_PATTERN = "reply+%s+code@site.io"

# The format of the email that is sent
EMAIL_FROM_PATTERN = u'''"%s en SITE" <%s>'''

# The secret key that is required to parse the email
EMAIL_REPLY_SECRET_KEY = "abc"

# The subject of the reply goes here
EMAIL_REPLY_SUBJECT = u"[site] %s"


SOCIALACCOUNT_PROVIDERS = {

    # 'facebook': {
    #    'SCOPE': ['email'],
    #    'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #    'METHOD': 'oauth2',
    #    'LOCALE_FUNC': lambda x: 'es_ES',
    #    'PROVIDER_KEY': get_env("FACEBOOK_PROVIDER_KEY"),
    #    'PROVIDER_SECRET_KEY': get_env("FACEBOOK_PROVIDER_SECRET_KEY"),
    # },

    # 'persona': {
    #    'REQUEST_PARAMETERS': {'siteName': 'Biostar'}
    # },

    # 'github': {
    #    'SCOPE': ['email'],
    #    'PROVIDER_KEY': get_env("GITHUB_PROVIDER_KEY"),
    #     'PROVIDER_SECRET_KEY': get_env("GITHUB_PROVIDER_SECRET_KEY"),
    #    },

    # 'google': {
    #    'SCOPE': ['email', 'https://www.googleapis.com/auth/userinfo.profile'],
    #    'AUTH_PARAMS': {'access_type': 'online'},
    #    'PROVIDER_KEY': get_env("GOOGLE_PROVIDER_KEY"),
    #    'PROVIDER_SECRET_KEY': get_env("GOOGLE_PROVIDER_SECRET_KEY"),
    # },

    # 'orcid': {
    #    'PROVIDER_KEY': get_env("ORCID_PROVIDER_KEY"),
    #    'PROVIDER_SECRET_KEY': get_env("ORCID_PROVIDER_SECRET_KEY"),
    # },
}


SITE_LOGO = "biostar2.logo.png"

DAILY_DIGEST_TITLE = '[site daily digest] %s'
WEEKLY_DIGEST_TITLE = '[site weekly digest] %s'


TEMPLATE_DIRS = ('org/bioconductor/templates',) + TEMPLATE_DIRS

STATICFILES_DIRS = ('org/bioconductor/static',) + STATICFILES_DIRS

TIME_ZONE = 'America/Lima'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

# Configure language detection
LANGUAGE_DETECTION = ['es']
