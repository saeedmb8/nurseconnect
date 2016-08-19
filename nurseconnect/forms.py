from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from molo.profiles.forms import RegistrationForm, EditProfileForm
from nurseconnect import constants


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
        label=_("Sex"),
        choices=constants.SEX,
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


class NurseConnectForgotPasswordForm(Form):
    pass


class NurseConnectResetPasswordForm(Form):
    pass


class NurseConnectEditProfileForm(EditProfileForm):
    pass
