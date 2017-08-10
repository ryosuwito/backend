#!/usr/bin/env bash
NUM_WORKERS=4
# /etc/init.d/postfix start
# cd /usr/src/app/
source env/bin/activate
pip install -r requirements.txt
export DJANGO_DEPLOYMENT=1
python manage.py migrate
python manage.py collectstatic --noinput
kill $(lsof -t -i:8888)
gunicorn dtlweb.wsgi:application --bind 0.0.0.0:8888 --name dtlweb_app -w $NUM_WORKERS
