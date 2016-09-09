from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

ZATEL_REG = r"^((?:\+27|27)|0)[\s-]?(\d{2})[\s-]?(\d{3})[\s-]?(\d{4})[\s]*$"
INT_PREFIX = "+27"


class RegistrationForm(forms.Form):
    username = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                ZATEL_REG,
                "Please enter a valid South African telephone number"
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "eg. 0821234567",
                "type": "tel",
                "zaTel": "true",
                "required": "required"
            }
        ),
        label=_("Mobile Number"),
    )

    password = forms.RegexField(
        regex=r"^\w+$",
        widget=forms.PasswordInput(
            attrs=dict(
                required=True,
                render_value=False,
                type="password",
                placeholder=_("Enter Password")
            )
        ),
        min_length=4,
        error_messages={
            "invalid": _(
                "Your password must contain any alphanumeric "
                "combination of 4 or more characters."
            ),
        },
        label=_("Password")
    )

    confirm_password = forms.RegexField(
        regex=r"^\w+$",
        widget=forms.PasswordInput(
            attrs=dict(
                required=True,
                render_value=False,
                type="password",
                placeholder=_("Confirm Password")
            )
        ),
        min_length=4,
        error_messages={
            "invalid": _(
                "Your password must contain any alphanumeric "
                "combination of 4 or more characters."
            ),
        },
        label=_("Password")
    )

    terms_and_conditions = forms.BooleanField(
        required=True,
        error_messages={
            "invalid": _(
                "Please accept the T&amp;Cs "
                "in order to complete the registration"
            )
        },
        label=_("Accept the Terms of Use")
    )

    def clean_username(self):

        if User.objects.filter(
            username__iexact=self.cleaned_data["username"]
        ).exists():
            raise forms.ValidationError(_("Username already exists."))
        username = self.cleaned_data["username"]

        if username and username[0] == "0":
            self.cleaned_data["username"] = \
                INT_PREFIX + username[1:len(username)]

        return self.cleaned_data["username"]

    def clean(self):
        password = self.cleaned_data.get("password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)
        if (password and confirm_password and
                (password == confirm_password)):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("Passwords do not match."))


class EditProfileForm(forms.Form):
    first_name = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Name"),
            }
        ),
        max_length=30
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Surname"),
            }
        ),
        max_length=30
    )

    username = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                ZATEL_REG,
                "Please enter a valid South African telephone number"
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "eg. 0821234567",
                "type": "tel",
                "zaTel": "true",
                "required": "required"
            }
        ),
        label=_("Mobile Number"),
    )
