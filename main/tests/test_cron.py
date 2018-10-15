#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mock

from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.core.files import File

from main import cron
from main.models import OnlineApplication, TestRequest
from main.cron import need_send_test_now, send_online_tests


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class CronTestCase(TestCase):
    def setUp(self):
        self.application = OnlineApplication(
            position=OnlineApplication.DEVELOPER,
            name="Yen Nguyen",
            email="ynguyen@dytechlab.com",
            resume=File(open(
                os.path.join(FIXTURE_DIR, 'sample_resume.txt')))
        )
        self.application.save()
        self.test_request = TestRequest(
            application=self.application
        )
        self.test_request.save()

    def test_need_send_test_now(self):
        # test request not set
        self.assertFalse(need_send_test_now(self.test_request))

        self.test_request.datetime = timezone.now()
        self.test_request.status = TestRequest.STATUS_SET
        self.test_request.save()
        self.assertTrue(need_send_test_now(self.test_request))

        self.test_request.datetime = timezone.now() + timedelta(minutes=10)
        self.test_request.save()
        self.assertFalse(need_send_test_now(self.test_request))

    @mock.patch('main.cron.send_test', mock.Mock())
    def test_send_online_tests(self):
        send_online_tests()
        cron.send_test.assert_not_called()

        self.test_request.datetime = timezone.now()
        self.test_request.status = TestRequest.STATUS_SET
        self.test_request.save()
        send_online_tests()
        cron.send_test.assert_any_call(self.test_request)
        self.assertEqual(TestRequest.objects.get(pk=self.test_request.pk).status,
                         TestRequest.STATUS_SENT)
