#!/usr/bin/env bash
set -e

PORT=$1

source env/bin/activate
pip install -r requirements.txt
# python manage.py makemigrations
python2 manage.py migrate
python2 manage.py collectstatic --noinput

# run crontab 2 times (since the first time may has conflict)
python2 manage.py crontab add
python2 manage.py crontab add

python2 manage.py runserver 0.0.0.0:8888
