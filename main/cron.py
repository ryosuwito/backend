#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import traceback
import logging

from django.utils import timezone
from datetime import timedelta, datetime

from models import TestRequest
from emails import send_test


logger = logging.getLogger(__name__)


def need_send_test_now(test_request):
    # when testrequest.status=set, and time now pass testrequest.datetime
    # NOTES: send earlier 5 minutes
    return test_request.status == TestRequest.STATUS_SET \
            and test_request.datetime \
            and timezone.now() + timedelta(minutes=5)  >= test_request.datetime


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
