DTL Website
=====================================

# Requirements
1. Python 2.7
2. Virtualenv

# Installation
```bash
git clone gitlab@10.200.79.103:ynguyen/dtl-website.git
cd dtl-website
./setup.sh
source env/bin/activate
python manage.py migrate

# create superuser (for login admin panel)
python manage.py createsuperuser

# setup cronjobs
python manage.py crontab add (see result, you may need to run several times to resolve conflicts)

```
# Run server locally
```
python manage.py runserver 8888
```

# Deploy to production
```
source env/bin/activate
export DJANGO_DEPLOYMENT=1

# setup cronjob
python manage.py crontab add (see result, you may need to run several times to resolve conflicts)

# run server (note that the port will be 8888)
./gunicorn/start.sh

# put all you test files (i.e developer-en.pdf) to ./media/ folder instead of ./main/media/ folder
```
