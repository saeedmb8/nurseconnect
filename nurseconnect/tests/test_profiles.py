from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from molo.core.tests.base import MoloTestCaseMixin


class UserProfileValidationTests(MoloTestCaseMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.mk_main()

    def test_user_profile_validation(self):
        response = self.client.post(reverse("user_register"), {
            "username": "wrong username",
            "password": "1234"
        })
        self.assertContains(response,
                            "Please enter a valid South "
                            "African telephone number")

        response = self.client.post(reverse("user_register"), {
            "username": "username",
            "password": "wrong$$$"
        })
        self.assertContains(response,
                            "Your password must contain any alphanumeric "
                            "combination of 4 or more characters.")

        response = self.client.post(reverse("user_register"), {
            "username": "username",
            "password": "12"
        })
        self.assertContains(response,
                            "Ensure this value has at least 4 characters"
                            " (it has 2).")

        self.user = User.objects.create_user(
            username="+27791234567",
            password="1234chris")

        response = self.client.post(reverse("molo.profiles:auth_login"), {
            "username": "wrong",
            "password": "1234chris",
        })
        self.assertContains(response,
                            "Your mobile number and password does not match. "
                            "Please try again.")

        response = self.client.post(reverse("molo.profiles:auth_login"), {
            "username": "tester",
            "password": "1234chris1234chris",
        })
        self.assertContains(response,
                            "Your mobile number and password does not match. "
                            "Please try again.")


class RegistrationViewTest(MoloTestCaseMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.mk_main()

    def test_user_info_displaying_after_registration(self):
        self.user = User.objects.create_user(
            username="+27791234567",
            password="tester1234")
        self.client.login(username="+27791234567", password="tester1234")
        response = self.client.get(reverse("edit_my_profile"))
        self.assertNotContains(response, "Rick")
        self.assertNotContains(response, "Morty")
        self.user.first_name = "Rick"
        self.user.last_name = "Morty"
        self.user.save()
        response = self.client.get(reverse("edit_my_profile"))
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "username")
