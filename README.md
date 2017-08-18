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

```
# Run server locally
```
source env/bin/activate

# setup cronjobs in development
python manage.py --settings=dtlweb.settings.dev crontab add (see result, you may need to run several times to resolve conflicts)

python manage.py runserver 8888
```

# Deploy to production
```
source env/bin/activate

# setup cronjob in production
python manage.py --settings=dtlweb.settings.prod crontab add (see result, you may need to run several times to resolve conflicts)

# run server
./gunicorn/start.sh

# put all you test files (i.e developer-en.pdf) to ./media/ folder instead of ./main/media/ folder
```
