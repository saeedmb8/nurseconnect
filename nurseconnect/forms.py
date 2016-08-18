from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from nurseconnect.constants import GENDERS
from molo.profiles.forms import RegistrationForm, EditProfileForm


class NurseConnectRegistrationForm(RegistrationForm):
    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=GENDERS,
        required=True
    )

    security_question_1_answer = forms.CharField(
        label=_("Anser to Security Question 1"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=128
            )
        ),
    )

    security_question_2_answer = forms.CharField(
        label=_("Anser to Security Question 2"),
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=128
            )
        ),
    )


class NurseConnectForgotPasswordForm(Form):
    pass
    # username = forms.RegexField(
    #     regex=r'^[\w.@+-]+$',
    #     widget=forms.TextInput(
    #         attrs=dict(
    #             required=True,
    #             max_length=30
    #         )
    #     ),
    #     label=_("Username"),
    #     error_messages={
    #         "invalid": _("This value must contain only letters, "
    #                      "numbers and underscores."),
    #     }
    # )
    #


class NurseConnectResetPasswordForm(Form):
    pass


class NurseConnectEditProfileForm(EditProfileForm):
    pass
