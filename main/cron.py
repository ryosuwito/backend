#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import logging
import requests
import jwt
import time as _time
import datetime
import pytz

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models import Q
from datetime import timedelta

from .models import (
    TestRequest,
    OpenJob,
)
from emails import send_test, send_token_email, send_reminding_test_email, send_on_token_failed


logger = logging.getLogger(__name__)
TOKEN_IN_QUEUE = 'TOKEN_IN_QUEUE'
TOKEN_SENT = 'TOKEN_SENT'
TOKEN_SEND_FAILED = 'TOKEN_SEND_FAILED'
_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=timezone.utc)

###
# TestRequest status
# (status, token_status)
# ('NEW', 'TOKEN_IN_QUEUE') or ('NEW', ''(created after Sept 2019))
# ('SET', 'TOKEN_IN_QUEUE')
# ('SET', 'TOKEN_SENT') | ('SET', 'TOKEN_SEND_FAILED')-> (end here)
# ('SENT', 'TOKEN_SENT') -> (end here)
###


def timestamp(dtime):
    "Return POSIX timestamp as float"
    if dtime.tzinfo is None:
        return _time.mktime((dtime.year, dtime.month, dtime.day,
                             dtime.hour, dtime.minute, dtime.second,
                             -1, -1, -1)) + dtime.microsecond / 1e6
    else:
        return (dtime - _EPOCH).total_seconds()


def need_send_test_now(test_request, minutes=5, send_after_datetime=True):
    # when testrequest.status=set, and time now pass testrequest.datetime
    # NOTES: send earlier 5 minutes
    if not send_after_datetime and timezone.now() >= test_request.datetime:
        return False

    return test_request.status == TestRequest.STATUS_SET \
        and test_request.datetime \
        and timezone.now() + timedelta(minutes=minutes) >= test_request.datetime


def send_online_tests():
    test_requests = TestRequest.objects.all()
    for req in test_requests:
        try:
            if need_send_test_now(req):
                # TODO: need to set status to SENDING to avoid email duplicate
                send_test(req)
                req.status = TestRequest.STATUS_SENT
                req.save()
        except:
            logger.error("{}: {}".format(req, traceback.format_exc()))


def send_on_remind_tests():
    """
    2019 Sept 16

    This crontab function will send a reminding email to participants 30 minutes before
    their online test start. The TestRequest's status will be set STATUS_SENT to indicate
    that the reminding email was sent but not the test as sent by email as before.
    """
    for req in TestRequest.objects.filter(token_status=TOKEN_SENT).filter(status__in=[TestRequest.STATUS_SET]):
        try:
            # If it's around 30 minutes before the test start
            if need_send_test_now(req, minutes=30, send_after_datetime=False):
                send_reminding_test_email(req, 30, online_test_host=settings.ONLINE_TEST_HOST)
                req.status = TestRequest.STATUS_SENT
                req.save()

            # If it's after the test start, the reminding email will not be sent and the status will be set STATUS_SET
            elif req.datetime < timezone.now():
                req.status = TestRequest.STATUS_SENT
                req.save()
        except:
            logger.error("{}: {}".format(req, traceback.format_exc()))


def send_test_token():
    test_requests = TestRequest.objects.filter(status=TestRequest.STATUS_SET)
    test_requests = test_requests.filter(~Q(token_status__in=[TOKEN_SENT, TOKEN_SEND_FAILED]))

    # Traverse all test_requests that is not marked as TOKEN_SENT or TOKEN_SEND_FAILED
    for req in test_requests:
        try:
            # Mark all test_requests with application created_at time before (2019, 9, 1, 0, 0, 0) TOKEN_SEND_FAILED
            # and do nothing with these. In other words, test_request will be mark TOKEN_SEND_FAILED if it's application
            # has created before Sep, 2019 and token_status is empty or None. If you want to create a token to an
            # application created before Sept 2019, you can set its token_status with non-empty like TOKEN_IN_QUEUE
            #
            if req.application.created_at < timezone.datetime(2019, 9, 1, 0, 0, 0, tzinfo=pytz.utc):
                if not req.token_status:
                    req.refresh_from_db()
                    req.token_status = TOKEN_SEND_FAILED
                    req.token = 'Application before Sep 2019'
                    req.save(update_fields=('token_status', 'token'))
                    continue

            # If this is more than 2 days before the test then skip this
            if req.allow_update() or req.test_site:
                continue

            app = req.application
            query = {
                'position': app.position,
                'typ': app.typ,
                'workplace': app.workplace,
            }
            open_job = OpenJob.objects.filter(**query).first()
            if open_job is None or not open_job.active:
                # Send out and email here
                req.refresh_from_db()
                req.token_status = TOKEN_SEND_FAILED
                req.token = 'There is no available open job for this application'
                req.save(update_fields=('token_status', 'token'))
                logger.error('There is no available open job for the application {}'.format(app.id))
                continue

            if not open_job.test_id:
                req.refresh_from_db()
                req.token_status = TOKEN_SEND_FAILED
                req.token = 'There is no test_id'
                req.save(update_fields=('token_status', 'token'))
                logger.error('There is no test_id assigned to the opening job id {}'.format(open_job.id))
                continue

            payload = {
                'username': get_random_string(10),
                'password': get_random_string(10),
                'timestamp': timestamp(timezone.now()),
                'start_time_timestamp': timestamp(req.datetime),
                'fullname': app.name,
                'test_id': open_job.test_id,
                'email': app.email,
            }
            token = jwt.encode(payload, settings.SHARE_KEY, 'HS256')
            url = settings.ONLINE_TEST_ACTIVE_USER_LINK(token)
            # Set token status failed anyway to avoid resend.
            req.refresh_from_db()
            req.token_status = TOKEN_SEND_FAILED
            req.token = 'Cannot active token'
            req.save(update_fields=('token_status', 'token'))

            res = requests.get(url)
            if res.status_code not in [200, 302]:
                send_on_token_failed(req.application)
                logger.error('Cannot active token for test_request {}'.format(req.id))
            else:
                req.refresh_from_db()
                req.token = token
                req.token_status = TOKEN_SENT
                req.save(update_fields=('token', 'token_status'))
                context = {
                    'username': payload['username'],
                    'password': payload['password'],
                    'host': settings.ONLINE_TEST_HOST,
                    'test_request': req,
                }
                send_token_email(context)
        except Exception as err:
            logger.error(err)
