# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Base configuration.
class BaseConfig(object):

    # main config
    SECRET_KEY = ''
    SECURITY_PASSWORD_SALT = ''
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # mail accounts
    MAIL_DEFAULT_SENDER = ''

# Development configuration.
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG_TB_ENABLED = True

# Testing configuration.
class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = ''

# Production configuration.
class ProductionConfig(BaseConfig):
    SECRET_KEY = ''
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG_TB_ENABLED = False
    STRIPE_SECRET_KEY = 'foo'
    STRIPE_PUBLISHABLE_KEY = 'bar'