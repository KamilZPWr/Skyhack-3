import os


class BaseConfig:
    TESTING = False
    CSRF_ENABLED = True


class TestingConfig(BaseConfig):
    TESTING = True
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_BROKER_URL = 'memory://'
    BROKER_BACKEND = 'memory://'
    BROKER_URL = CELERY_BROKER_URL


class ProductionConfig(BaseConfig):
    TESTING = False
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    BROKER_URL = CELERY_BROKER_URL


class Config:
    config = {
        'testing': TestingConfig,
        'production': ProductionConfig,
    }
