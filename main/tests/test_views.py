from django.urls import reverse
from django.test import TestCase
from main.forms import OnlineApplicationForm, InternApplicationForm


class OnlineApplicationViewTest(TestCase):
    def setUp(self):
        self.app = None

    def test_career_apply_successful(self):
        form = OnlineApplicationForm(instance=self.app)
        response = self.client.post(reverse('main.career.apply'), {'form': form})
        self.assertEquals(response.status_code, 200)
        # test response contain confirm_msg
        # test handle_application_form called once

    def test_career_apply_intern_successful(self):
        form = InternApplicationForm(instance=self.app)
        response = self.client.post(reverse('main.career.apply_intern'), {'form': form})
        self.assertEquals(response.status_code, 200)
        # test response contain confirm_msg
        # test handle_application_form called once

    def test_career_apply_unsuccessful(self):
        # if form not valid
        pass

    def test_handle_application_form(self):
        # call send_online_application_confirm once
        # call send_online_application_confirm once
        pass


class TestRequestViewTest(TestCase):
    def setUp(self):
        pass

    def test_retrieve_testrequest(self):
        pass

    def test_update_testrequest(self):
        # modify datetime
        pass
