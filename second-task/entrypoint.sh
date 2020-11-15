#!/bin/sh

if [ "$1" = 'dashboard' ]; then
    gunicorn -w 2 -b 0.0.0.0:8050 dashboard.app_drop:app --preload
fi
