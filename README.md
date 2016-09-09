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
python manage.py runserver
```

# Run website on localhost (for ftang & mhua)
```bash
git pull origin master
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
* Close any page with localhost:8000 you opened before
* Open your browser (in incognito or private mode): localhost:8000
* Remember to open in private mode browser to avoid css caching 

