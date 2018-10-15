#!/usr/bin/env bash
set -e

PORT=$1

source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# run crontab 2 times (since the first time may has conflict)
python manage.py crontab add
python manage.py crontab add

python manage.py runserver 0.0.0.0:8888
