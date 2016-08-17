from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db import models

from nurseconnect import constants


class NurseConnectUserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="nurse_connect_profile",
        primary_key=True
    )
    gender = models.CharField(
        max_length=1,
        choices=constants.GENDERS,
        blank=True,
        null=True
    )
    mobile_number = models.CharField(
        max_length=15
    )
    staff_number = models.CharField(
        max_length=15
    )
    facility_code = models.CharField(
        max_length=15
    )
    security_question_1_answer = models.CharField(
        max_length=128,
        null=True
    )
    security_question_2_answer = models.CharField(
        max_length=128,
        null=True
    )

    # based on django.contrib.auth.models.AbstractBaseUser set_password &
    # check_password functions (takes plain text, generates hash for database)
    def set_security_question_1_answer(self, raw_answer):
        self.security_question_1_answer = make_password(
            raw_answer.strip().lower()
        )

    def set_security_question_2_answer(self, raw_answer):
        self.security_question_2_answer = make_password(
            raw_answer.strip().lower()
        )

    def check_security_question_1_answer(self, raw_answer):
        def setter(raw_answer):
            self.set_security_question_1_answer(raw_answer)
            self.save(update_fields=["security_question_1_answer"])

        return check_password(
            raw_answer.strip().lower(), self.security_question_1_answer, setter
        )




