import os


class BaseConfig:
    TESTING = False
    CSRF_ENABLED = True

    CLEANER_INTERVAL = int(os.environ.get('CLEANER_INTERVAL', 86400))
    # CELERY_IMPORTS = ()     # TODO: add celery task here
    # CELERYBEAT_SCHEDULE = {
    #     'cleaner_task': {
    #         'task': 'clear_data',
    #         'schedule': timedelta(seconds=CLEANER_INTERVAL)
    #     },
    # }


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
