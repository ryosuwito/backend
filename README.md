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
./gunicorn/start.sh
```
