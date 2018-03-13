DTL Website
=====================================

# Requirements
1. Python 2.7

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

python manage.py runserver <port>

# setup cronjobs in development
# pls see result, you may need to run several times to resolve conflicts
python manage.py crontab add --settings=dtlweb.settings.dev

```

# Deploy to production
```
source env/bin/activate

# run server
./gunicorn/start.sh

# setup cronjob in production
# pls see result, you may need to run several times to resolve conflicts
python manage.py crontab add --settings=dtlweb.settings.prod

# put all you test files (i.e developer-en.pdf, ...) to ./media/ folder.
```

# Run unittest
```
source env/bin/activate

python manage.py test main.tests
```

# TODO
- Test, CI
- limit log file size
