#!/usr/bin/env bash
NUM_WORKERS=4
/etc/init.d/postfix start
cd /usr/src/app/
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn dtlweb.wsgi:application --bind 0.0.0.0:8888 --name dtlweb_app -w $NUM_WORKERS
