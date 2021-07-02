import os


class BaseConfig:
    ENV = 'development'
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'microservice'
    SEND_FILE_MAX_AGE_DEFAULT = 0


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://david:password@localhost:5432/david")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']  # allow blacklisting for access and refresh tokens


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGODB_SETTINGS = {
        'host': os.environ.get("PROD_DATABASE_URL", "mongodb://localhost:27017/app-testing")
    }


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = True
    JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
