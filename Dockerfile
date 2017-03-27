FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y postfix
RUN apt-get install -y libssl-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y python python-pip python-dev
# disable ipv6 for postfix to avoid a bunch of problems
RUN sed -i 's/inet_protocols *= *all/inet_protocols = ipv4/g' /etc/postfix/main.cf
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD . /usr/src/app/
RUN mkdir -p /var/run/gunicorn
RUN mkdir -p /var/log/gunicorn
RUN mkdir -p /var/log/app
RUN mkdir -p /usr/src/app/run
