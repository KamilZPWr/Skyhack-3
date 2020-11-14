from service.api import app
from service.factory import create_celery

flask = app
celery = create_celery(app)

if __name__ == '__main__':
    flask.run()
