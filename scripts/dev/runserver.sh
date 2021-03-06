#!/usr/bin/env bash
set -e

PORT=$1

pip install -r requirements.txt
# python manage.py makemigrations
python2 manage.py migrate

# run crontab 2 times (since the first time may has conflict)
python2 manage.py crontab add
python2 manage.py crontab add

DJANGO_SETTINGS_MODULE=dtlweb.settings.dev python2 manage.py runserver 0.0.0.0:8001
