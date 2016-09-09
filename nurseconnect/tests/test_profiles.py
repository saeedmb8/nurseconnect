from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from molo.core.tests.base import MoloTestCaseMixin


class UserProfileValidationTests(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.client = Client()

    def test_user_profile_validation(self):
        response = self.client.post(reverse("user_register"), {
            "username": "wrong username",
            "password": "1234",
            "confirm_password": "1234",
            "terms_and_conditions": True
        })
        self.assertContains(response,
                            "Please enter a valid South "
                            "African telephone number")

        response = self.client.post(reverse("user_register"), {
            "username": "username",
            "password": "wrong$$$",
            "confirm_password": "1234",
            "terms_and_conditions": True
        })
        self.assertContains(response,
                            "This value must contain only alphanumeric characters.")

        response = self.client.post(reverse("user_register"), {
            "username": "username",
            "password": "12",
            "confirm_password": "1234",
            "terms_and_conditions": True
        })
        self.assertContains(response,
                            "Ensure this value has at least 4 characters"
                            " (it has 2).")

        self.user = User.objects.create_user(
            username="0795265739",
            password="1234chris")

        response = self.client.post(reverse("molo.profiles:auth_login"), {
            "username": "wrong",
            "password": "1234chris",
        })
        self.assertContains(response,
                            "Your username and password does not match."
                            " Please try again.")

        response = self.client.post(reverse("molo.profiles:auth_login"), {
            "username": "tester",
            "password": "1234chris1234chris",
        })
        self.assertContains(response,
                            "Your username and password does not match."
                            " Please try again.")


class RegistrationViewTest(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.client = Client()

    def test_user_info_displaying_after_registration(self):
        self.user = User.objects.create_user(
            username='0791234567',
            password='tester1234')
        self.client.login(username='0791234567', password='tester1234')
        response = self.client.get(reverse('edit_my_profile'))
        self.assertNotContains(response, 'first_name')
        self.assertNotContains(response, 'last_name')
        self.user.first_name = 'Rick'
        self.user.last_name = 'Morty'
        self.user.save()
        response = self.client.get(reverse('edit_my_profile'))
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'username')
