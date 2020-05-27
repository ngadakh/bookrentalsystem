import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


DEFAULT_SERVER = '0.0.0.0'
DEFAULT_SERVER_PORT = 5000
LOG_FILE = os.path.join(BASEDIR, 'brs.log')
SQLITE_PATH = os.path.join(BASEDIR, 'brs.db')
TEST_SQLITE_PATH = os.path.join(BASEDIR, 'test_brs.db')

