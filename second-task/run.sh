#!/bin/bash

# Setup SSL
export STORAGE_PATH="storage"


export PYTHONUNBUFFERED=True

WORKERS_NUM=4


gunicorn "service.api:app" --chdir ${PWD} --workers ${WORKERS_NUM} --worker-class gevent --worker-connections 1000 -b 0.0.0.0:5000 --timeout 600
