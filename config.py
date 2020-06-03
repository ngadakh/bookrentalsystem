import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "secretkey"
    DEFAULT_SERVER = '0.0.0.0'
    DEFAULT_SERVER_PORT = 5000
    LOG_FILE = os.path.join(BASEDIR, 'brs.log')
    USERS = {'username': 'admin', 'password': 'admin'}


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLITE_PATH = os.path.join(BASEDIR, 'brs.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLITE_PATH = os.path.join(BASEDIR, 'test_brs.db')


ENVIRONMENT = DevelopmentConfig
# ENVIRONMENT = TestingConfig
