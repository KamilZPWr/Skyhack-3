from celery import Celery
from flask import Flask

from service.config import Config


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config.config[environment])
    return app


def create_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery
