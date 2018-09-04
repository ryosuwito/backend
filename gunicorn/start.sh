#!/usr/bin/env bash
set -e
NUM_WORKERS=16
PORT=80
# /etc/init.d/postfix start
# cd /usr/src/app/
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# run crontab 2 times (since the first time may has conflict)
python manage.py crontab add --settings=dtlweb.settings.prod
python manage.py crontab add --settings=dtlweb.settings.prod

kill $(lsof -t -i:$PORT) || true
gunicorn dtlweb.wsgi:application --bind 0.0.0.0:$PORT --name dtlweb_app -w $NUM_WORKERS
