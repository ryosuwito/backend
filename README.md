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

python manage.py runserver <port> --settings=dtlweb.settings.dev

# Open manage.py, change default environment to development
# manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtlweb.settings.dev")

# Run server
./scripts/dev/runserver.sh

```

# Deploy to production
```
source env/bin/activate

# run server
./gunicorn/start.sh

# put all you test files (i.e developer-en.pdf, ...) to ./media/ folder.

# setup cronjob in production
# pls see result, you may need to run several times to resolve conflicts
```


# Update test files

- Check configuration in `dtlweb/settings/prod.py`.
- Currently all test files are kept in `media/` folder, and put to git repository too
in order to have version control of those test files.

- To update, just replace the file in `media/` folder, push to git and pull the change
on the deployment server.


# Other Notes

- Resumes are kepts in `media/resumes` folder.


# Run unittest
```
source env/bin/activate

python manage.py test main.tests
```

# TODO
- Test, CI
- limit log file size
