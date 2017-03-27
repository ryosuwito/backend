#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import mock
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.core.files import File

from main import models

from main.models import OnlineApplication, TestRequest
from main.emails import send_test_request, send_reject

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class OnlineApplicationTestCase(TestCase):
    def setUp(self):
        self.application = OnlineApplication(
            position=OnlineApplication.DEVELOPER,
            name="Yen Nguyen",
            email="ynguyen@dytechlab.com",
            resume=File(open(
                os.path.join(FIXTURE_DIR, 'sample_resume.txt')))
        )
        self.application.save()


    @mock.patch('main.models.OnlineApplication.on_update_status', mock.Mock())
    def test_save_not_trigger_on_update_status_if_status_unchange(self):
        self.application.status = OnlineApplication.APP_STATUS_NEW
        self.application.save()
        self.application.on_update_status.assert_not_called()

    @mock.patch('main.models.OnlineApplication.on_update_status', mock.Mock())
    def test_save_trigger_on_update_status_if_status_change(self):
        self.application.status = OnlineApplication.APP_STATUS_PASS_RESUME
        self.application.save()
        self.application.on_update_status.assert_called_once_with()

    @mock.patch('main.models.send_test_request', mock.Mock())
    def test_on_update_status_to_PASS_RESUME(self):
        with self.assertRaises(TestRequest.DoesNotExist):
            test_request = TestRequest.objects.get(application=self.application)

        self.application.status = OnlineApplication.APP_STATUS_PASS_RESUME
        self.application.on_update_status()

        test_request = TestRequest.objects.get(application=self.application)
        self.assertIsNotNone(test_request)

        models.send_test_request.assert_called_once_with(test_request)

    @mock.patch('main.models.send_reject', mock.Mock())
    def test_on_update_status_to_FAIL_RESUME(self):
        send_reject = mock.Mock()
        self.application.status = OnlineApplication.APP_STATUS_FAIL_RESUME
        self.application.on_update_status()
        models.send_reject.assert_called_once_with(self.application)

    @mock.patch('main.models.send_reject', mock.Mock())
    def test_on_update_status_to_FAIL_TEST(self):
        send_reject = mock.Mock()
        self.application.status = OnlineApplication.APP_STATUS_FAIL_TEST
        self.application.on_update_status()
        models.send_reject.assert_called_once_with(self.application)


class TestRequestTestCase(TestCase):
    def setUp(self):
        self.application = OnlineApplication(
            position=OnlineApplication.DEVELOPER,
            name="Yen Nguyen",
            email="ynguyen@dytechlab.com",
            resume=File(open(
                os.path.join(FIXTURE_DIR, 'sample_resume.txt')))
        )
        self.application.save()

    def test_create_test_request_for_application(self):
        test_request = TestRequest.createTestRequestForApplication(self.application)
        self.assertIsNotNone(TestRequest.objects.get(pk=test_request.pk))
        self.assertEqual(test_request.application, self.application)

        # if test_request already exist
        test_request_again = TestRequest.createTestRequestForApplication(self.application)
        self.assertEqual(test_request.pk, test_request_again.pk)

    def test_allow_update(self):
        # now STATUS_NEW
        test_request = TestRequest(
            status=TestRequest.STATUS_NEW
        )
        self.assertTrue(test_request.allow_update())

        test_request.status = TestRequest.STATUS_SENT
        self.assertFalse(test_request.allow_update())

        test_request.status = TestRequest.STATUS_SET
        test_request.datetime = timezone.now() + timedelta(days=3)
        self.assertTrue(test_request.allow_update())
        test_request.datetime = timezone.now() + timedelta(days=2)
        self.assertTrue(test_request.allow_update())
        test_request.datetime = timezone.now() + timedelta(days=1)
        self.assertFalse(test_request.allow_update())

    def test_get_test_filepath(self):
        from django.conf import settings

        application = OnlineApplication(
            position=OnlineApplication.DEVELOPER
        )
        test_request = TestRequest(
            application=application,
            version = TestRequest.VER_ENGLISH
        )
        self.assertEqual(test_request.get_test_filepath(), settings.TEST_FILES['DEV']['EN'])

        application.position = OnlineApplication.Q_RESEARCHER
        self.assertEqual(test_request.get_test_filepath(), settings.TEST_FILES['QRES']['EN'])

        application.position = OnlineApplication.FQ_RESEARCHER
        self.assertEqual(test_request.get_test_filepath(), settings.TEST_FILES['FQRES']['EN'])

        test_request.version = TestRequest.VER_CHINESE
        self.assertEqual(test_request.get_test_filepath(), settings.TEST_FILES['FQRES']['CN'])

