from django.test import TestCase

from nurseconnect.forms import RegistrationForm
from molo.core.tests.base import MoloTestCaseMixin


class RegisterTestCase(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()

    def test_register_username_required(self):
        form_data = {
            "password": "1234",
            "confirm_password": "1234",
            "terms_and_conditions": True
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_register_password_required(self):
        form_data = {
            "username": "+27791234567",
            "confirm_password": "1234",
            "terms_and_conditions": True
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_confirm_password_required(self):
        form_data = {
            "username": "+27791234567",
            "password": "1234",
            "terms_and_conditions": True
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
