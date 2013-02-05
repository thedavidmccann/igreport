#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

HOTLINE_NAME_QUESTION = "Thanks for your report, please send us ONLY the name of the person or organization you're reporting on?"
HOTLINE_AMOUNT_QUESTION = "What amount of money was involved?"
HOTLINE_WHEN_QUESTION = "When did the event you are reporting happen?"
HOTLINE_DISTRICT_QUESTION = "Please send us ONLY the name of your district?"
HOTLINE_SUBCOUNTY_QUESTION = "Please send us ONLY the name of your sub county?"
HOTLINE_CONFIRMATION_MESSAGE = "Your report has been recorded. Thank you."
CMS_USER = 'IGG developer'
CMS_PASSWORD = 'uncooperative'
CMS_URL = 'localhost:8008/sync/'

# -------------------------------------------------------------------- #
#                          PATH CONFIGURATION                          #
# -------------------------------------------------------------------- #

import sys, os

filedir = os.path.dirname(__file__)
sys.path.append(os.path.join(filedir))
sys.path.append(os.path.join(filedir, 'rapidsms', 'lib'))
sys.path.append(os.path.join(filedir, 'rapidsms_httprouter_src'))
sys.path.append(os.path.join(filedir, 'rapidsms_generic'))
sys.path.append(os.path.join(filedir, 'rapidsms_polls'))
sys.path.append(os.path.join(filedir, 'rapidsms_script'))
sys.path.append(os.path.join(filedir, 'django_eav'))
sys.path.append(os.path.join(filedir, 'igreport_src'))

# -------------------------------------------------------------------- #
#                          MAIN CONFIGURATION                          #
# -------------------------------------------------------------------- #
TIME_ZONE = "Africa/Kampala"  # "America/New_York"

ADMINS = (
)

# you should configure your database here before doing any real work.
# see: http://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': 'igreport',
        'HOST': 'dbserver',
        'USER': 'postgres',
    }
}

# the rapidsms backend configuration is designed to resemble django's
# database configuration, as a nested dict of (name, configuration).
#
# the ENGINE option specifies the module of the backend; the most common
# backend types (for a GSM modem or an SMPP server) are bundled with
# rapidsms, but you may choose to write your own.
#
# all other options are passed to the Backend when it is instantiated,
# to configure it. see the documentation in those modules for a list of
# the valid options for each.
INSTALLED_BACKENDS = {
    "message_tester": {
        "ENGINE": "rapidsms.backends.bucket",
    },
}


# to help you get started quickly, many django/rapidsms apps are enabled
# by default. you may wish to remove some and/or add your own.
INSTALLED_APPS = [
    "djtables",
    "mptt",
    "django_extensions",
    "rapidsms.contrib.handlers",

    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.staticfiles",

    # the rapidsms contrib apps.
    "rapidsms.contrib.default",
    "rapidsms.contrib.locations",
    "rapidsms.contrib.locations.nested",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.registration",
    "eav",
    "rapidsms_httprouter",
    "generic",
    "poll",
    "script",
    "rapidsms",
    "igreport",
]

SMS_APPS = [
    "igreport",
    "script",
    "poll",
]

STATIC_ROOT = '/opt/static/'
STATIC_URL = '/static/'

AUTH_PROFILE_MODULE = 'igreport.UserProfile'
LOCATION_POLL_VALID_TYPES = ['district']
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# this rapidsms-specific setting defines which views are linked by the
# tabbed navigation. when adding an app to INSTALLED_APPS, you may wish
# to add it here, also, to expose it in the rapidsms ui.
RAPIDSMS_TABS = [
#     ("rapidsms-dashboard", "Home"),
]

AUTHENTICATED_TABS = [
#    ("messagelog", "Message Log"),
]

# -------------------------------------------------------------------- #
#                         BORING CONFIGURATION                         #
# -------------------------------------------------------------------- #


# debug mode is turned on as default, since rapidsms is under heavy
# development at the moment, and full stack traces are very useful
# when reporting bugs. don't forget to turn this off in production.
DEBUG = TEMPLATE_DEBUG = True

# after login (which is handled by django.contrib.auth), redirect to the
# dashboard rather than 'accounts/profile' (the default).
LOGIN_REDIRECT_URL = "/"


# use django-nose to run tests. rapidsms contains lots of packages and
# modules which django does not find automatically, and importing them
# all manually is tiresome and error-prone.
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"


# for some reason this setting is blank in django's global_settings.py,
# but it is needed for static assets to be linkable.
# MEDIA_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"

# this is required for the django.contrib.sites tests to run, but also
# not included in global_settings.py, and is almost always ``1``.
# see: http://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1

# this is used for geoserver to tell which website this viz should be for (and prevents clashing of
# polls across different websites with the same id
DEPLOYMENT_ID = 1

# model containing blacklisted contacts
BLACKLIST_MODEL = "unregister.Blacklist"

# these weird dependencies should be handled by their respective apps,
# but they're not, so here they are. most of them are for django admin.
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
]

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

# -------------------------------------------------------------------- #
#                           HERE BE DRAGONS!                           #
#        these settings are pure hackery, and will go away soon        #
# -------------------------------------------------------------------- #

# these apps should not be started by rapidsms in your tests, however,
# the models and bootstrap will still be available through django.
TEST_EXCLUDED_APPS = [
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rapidsms",
    "rapidsms.contrib.ajax",
    "rapidsms.contrib.httptester",
]


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# the project-level url patterns
ROOT_URLCONF = "urls"

ALLOWED = (
    r'/accounts/login(.*)$',
    r'/accounts/logout(.*)$',
    r'/static/(.*)$',
    r'^/$',
    r'/about/$',
    r'/signup/$',
    r'^/bestviz(.*)'

    )

# AUTHENTICATION_BACKENDS = (
#    'django.contrib.auth.backends.ModelBackend',
#    'permission.backends.RoleBackend',
#    'permission.backends.PermissionBackend',
#    )
# south stuff
SOUTH_TESTS_MIGRATE = False

USE_I18N = True
INITIAL_USSD_SCREEN = 'ussd_root'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# since we might hit the database from any thread during testing, the
# in-memory sqlite database isn't sufficient. it spawns a separate
# virtual database for each thread, and syncdb is only called for the
# first. this leads to confusing "no such table" errors. We create
# a named temporary instance instead.
import os
import tempfile
import sys

try:
    if os.environ.has_key('LOCAL_SETTINGS'):
        # the LOCAL_SETTINGS environment variable is used by the build server
        sys.path.insert(0, os.path.dirname(os.environ['LOCAL_SETTINGS']))
        from settings_test import *
    else:
        from localsettings import *
except ImportError:
    pass
if 'test' in sys.argv:
    for db_name in DATABASES:
        DATABASES[db_name]['TEST_NAME'] = os.path.join(
            tempfile.gettempdir(),
            "%s.igreport.test.sqlite3" % db_name)

