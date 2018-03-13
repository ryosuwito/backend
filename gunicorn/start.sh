#!/usr/bin/env bash
NUM_WORKERS=16
# /etc/init.d/postfix start
# cd /usr/src/app/
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
kill $(lsof -t -i:80)
gunicorn dtlweb.wsgi:application --bind 0.0.0.0:80 --name dtlweb_app -w $NUM_WORKERS
