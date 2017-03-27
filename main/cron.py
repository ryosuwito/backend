#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback

from django.utils import timezone

from models import TestRequest
from emails import send_test


def need_send_test_now(test_request):
    # when testrequest.status=set, and time now pass testrequest.datetime
    return test_request.status == TestRequest.STATUS_SET \
            and test_request.datetime \
            and timezone.now() >= test_request.datetime


def send_online_tests():
    print 'Scan TestRequest database and send test file to candidates via email.'
    test_requests = TestRequest.objects.all()
    for req in test_requests:
        try:
            if need_send_test_now(req):
                send_test(req)
                req.status = TestRequest.STATUS_SENT
                req.save()
        except:
            pass
