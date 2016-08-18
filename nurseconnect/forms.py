import re

from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from nurseconnect.constants import GENDERS
from molo.profiles.forms import RegistrationForm, EditProfileForm
from nurseconnect.settings import REGEX_EMAIL
from nurseconnect.settings import REGEX_PHONE


def validate_no_email_or_phone(input):
    regexes = [REGEX_EMAIL, REGEX_PHONE]
    for regex in regexes:
        match = re.search(regex, input)
        if match:
            return False

    return True


class NurseConnectRegistrationForm(RegistrationForm):
    first_name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_lenght=30
            )
        ),
    )

    last_name = forms.CharField(
        label=_("Surname"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_lenght=30
            )
        ),
    )

    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=GENDERS,
        required=True
    )

    staff_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Staff Number",
                "minlength": "6",
                "maxlength": "9"
            }
        )
    )

    facility_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Facility Code",
                "minlength": "6",
                "maxlength": "9"
            }
        )
    )

    security_question_1_answer = forms.CharField(
        label=_("Anwser to Security Question 1"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=128
            )
        ),
    )

    security_question_2_answer = forms.CharField(
        label=_("Anwser to Security Question 2"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=128
            )
        ),
    )

    def clean_username(self):
        username = super(NurseConnectRegistrationForm, self).clean_username()

        if not validate_no_email_or_phone(username):
            raise forms.ValidationError(
                _(
                    "Sorry, but that is an invalid username. Please don't use"
                    " your email address or phone number in your username."
                )
            )
        return username


class NurseConnectForgotPasswordForm(Form):
    pass


class NurseConnectResetPasswordForm(Form):
    pass


class NurseConnectEditProfileForm(EditProfileForm):
    pass


class ReportCommentForm(Form):
    CHOICES = (
        ('Spam', _('Spam')),
        ('Offensive Language', _('Offensive Language')),
        ('Bullying', _('Bullying')),
        ('Other', _('Other'))
    )

    report_reason = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES
    )