:!/usr/bin/env bash
set -e

if [ ! -d "env" ]; then

  virtualenv=virtualenv-13.1.2
  mkdir env
  cd env
  wget https://pypi.python.org/packages/source/v/virtualenv/$virtualenv.tar.gz
  tar xvf $virtualenv.tar.gz
  cd $virtualenv
  python virtualenv.py ..
  cd ../..
  source env/bin/activate
  pip install -r requirements.txt
fi
