"""
NetBox configuration for testing {{ cookiecutter.project_name }}.

This configuration is used when running tests and should not be used in production.

Usage:
    export NETBOX_CONFIGURATION=testing.configuration
    python manage.py test {{ cookiecutter.underscored }}.tests
"""

import os

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'netbox'),
        'USER': os.getenv('DB_USER', 'netbox'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'netbox'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 300,
    }
}

# Redis configuration
REDIS = {
    'tasks': {
        'HOST': os.getenv('REDIS_HOST', 'localhost'),
        'PORT': int(os.getenv('REDIS_PORT', 6379)),
        'PASSWORD': os.getenv('REDIS_PASSWORD', ''),
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': os.getenv('REDIS_HOST', 'localhost'),
        'PORT': int(os.getenv('REDIS_PORT', 6379)),
        'PASSWORD': os.getenv('REDIS_PASSWORD', ''),
        'DATABASE': 1,
        'SSL': False,
    },
}

# Security settings (test-only values)
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# For testing, allow all hosts
ALLOWED_HOSTS = ['*']

# Enable debug mode for testing
DEBUG = True

# Plugin configuration
PLUGINS = [
    '{{ cookiecutter.underscored }}',
]

PLUGINS_CONFIG = {
    '{{ cookiecutter.underscored }}': {
        # Add any plugin configuration needed for testing
    },
}

# Disable SSL redirect for testing
SECURE_SSL_REDIRECT = False

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        '{{ cookiecutter.underscored }}': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# RQ (background task) configuration
RQ_QUEUES = {
    'default': {
        'HOST': os.getenv('REDIS_HOST', 'localhost'),
        'PORT': int(os.getenv('REDIS_PORT', 6379)),
        'DB': 0,
        'PASSWORD': os.getenv('REDIS_PASSWORD', ''),
        'SSL': False,
        'DEFAULT_TIMEOUT': 300,
    },
}

# Time zone
TIME_ZONE = 'UTC'

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/netbox_media'

# Session configuration
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email configuration (for testing only)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_SERVER = 'localhost'
EMAIL_PORT = 25
EMAIL_TIMEOUT = 10
EMAIL_FROM_EMAIL = 'netbox@localhost'

# Exempt all views from login requirement for testing
EXEMPT_VIEW_PERMISSIONS = ['*']

# Banner (optional)
BANNER_TOP = ''
BANNER_BOTTOM = ''

# Pagination
PAGINATE_COUNT = 50
MAX_PAGE_SIZE = 1000

# Prefer IPv4 for testing
PREFER_IPV4 = True

# GraphQL
GRAPHQL_ENABLED = True

# Changelog retention
CHANGELOG_RETENTION = 90

# Job result retention
JOBRESULT_RETENTION = 90

# Maps
MAPS_URL = 'https://maps.google.com/?q='

# Remote auth (disabled for testing)
REMOTE_AUTH_ENABLED = False
REMOTE_AUTH_BACKEND = 'netbox.authentication.RemoteUserBackend'
REMOTE_AUTH_HEADER = 'HTTP_REMOTE_USER'
REMOTE_AUTH_AUTO_CREATE_USER = True
REMOTE_AUTH_DEFAULT_GROUPS = []
REMOTE_AUTH_DEFAULT_PERMISSIONS = {}

# Maintenance mode
MAINTENANCE_MODE = False

# Storage
STORAGE_BACKEND = None
STORAGE_CONFIG = {}
