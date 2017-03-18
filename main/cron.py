#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from models import TestRequest


def need_send_email(test_request):
    # when testrequest.status=set, and time now pass testrequest.datetime
    return test_request.status == TestRequest.STATUS_SET \
            and test_request.datetime
            and datetime.now() >= TestRequest.datetime


def send_online_tests():
    print 'Scan TestRequest database and send test file to candidates via email.'
    test_requests = TestRequest.objects.all()
    for req in test_requests:
        if need_send_email(req):
            send_test()
            # update status of test request to be "SENT"
            req.status = TestRequest.STATUS_SENT
            req.save()

