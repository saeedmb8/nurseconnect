from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from molo.core.tests.base import MoloTestCaseMixin


class UserProfileTests(MoloTestCaseMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.mk_main()

    def test_user_profile_validation(self):
        # Username is expected to be a South African number,
        # normalised to +27 country code
        response = self.client.post(reverse("user_register"), {
            "username": "wrong username",
            "password": "1234",
            "confirm_password": "1234"
        })
        self.assertFormError(
            response, "form", "username",
            [u"Enter a valid phone number."]
        )

        # Passwords with non-alphanumeric characters raise errors
        response = self.client.post(reverse("user_register"), {
            "username": "0820000000",
            "password": "wrong$$$",
        })
        self.assertFormError(
            response, "form", "username",
            None
        )
        self.assertFormError(
            response, "form", "password",
            [u"Your password must contain any alphanumeric "
             u"combination of 4 or more characters."]
        )

        # Phone number starting with zero gives no errors
        response = self.client.post(
            reverse("user_register"),
            {
                "username": "0820000000",
                "password": "1234",
                "confirm_password": "1234",
                "terms_and_conditions": True,
            },
            follow=True
        )
        self.assertRedirects(response, reverse("home"))

        # Phone number starting with +27 gives no errors
        response = self.client.post(
            reverse("user_register"),
            {
                "username": "+2782111111",
                "password": "1234",
                "confirm_password": "1234",
                "terms_and_conditions": True,
            },
            follow=True
        )
        self.assertRedirects(response, reverse("home"))

        # User already exists
        user = User.objects.create_user(
            username="+27791234567",
            password="1234"
        )
        response = self.client.post(
            reverse("user_register"),
            {
                "username": "+27791234567",
                "password": "1234",
            }
        )
        self.assertFormError(
            response, "form", "username",
            [u"Username already exists."]
        )

    def test_login(self):
        pass