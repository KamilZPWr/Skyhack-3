#!/bin/bash

# Setup SSL
export STORAGE_PATH="storage"
if [ -z ${USE_HTTPS+x} ]
then
  USE_SSL=false
else
  python ./utils/get_keyvault_var.py OCR-SSL-CERT
  python ./utils/get_keyvault_var.py OCR-SSL-KEY
  echo `cat OCR-SSL-CERT` | base64 --decode > cert.pem
  echo `cat OCR-SSL-KEY` | base64 --decode > key.pem
  USE_SSL=true
fi

if [ ${USE_SSL} = true ]
then
  SSL_PARAM='--certfile=cert.pem --keyfile=key.pem --ciphers TLSv1.2'
fi

export PYTHONUNBUFFERED=True

WORKERS_NUM=4
if [ ! -z ${OCR_WORKERS_NUMBER+x} ]
then
  WORKERS_NUM=${OCR_WORKERS_NUMBER}
fi

gunicorn "service.api:app" --chdir ${PWD} --workers ${WORKERS_NUM} --worker-class gevent --worker-connections 1000 -b 0.0.0.0:5000 --timeout 600 ${SSL_PARAM}
