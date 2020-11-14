import os

from service.factory import create_app, create_celery


def register_blueprint(application):
    from service.api.endpoints import api_blueprint
    application.register_blueprint(api_blueprint)
    return application


app = create_app(os.environ.get('ENV', 'production'))
celery = create_celery(app)
logger = app.logger
app = register_blueprint(app)
