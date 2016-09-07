from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from molo.profiles import forms as molo_profiles_forms
from molo.profiles.models import UserProfile


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=30,
            )
        ),
        label=_("Username"),
        error_messages={
            'invalid': _("This value must contain only letters, "
                         "numbers and underscores."),
        }
    )
    password = forms.RegexField(
        regex=r'^\d{4}$',
        widget=forms.PasswordInput(
            attrs=dict(
                required=True,
                render_value=False,
                type='password',
            )
        ),
        max_length=4,
        min_length=4,
        error_messages={
            'invalid': _("This value must contain only numbers."),
        },
        label=_("PIN")
    )
    terms_and_conditions = forms.BooleanField(required=True)
    next = forms.CharField(required=False)

    def clean_username(self):
        validation_msg_fragment = molo_profiles_forms.get_validation_msg_fragment()

        if User.objects.filter(
            username__iexact=self.cleaned_data['username']
        ).exists():
            raise forms.ValidationError(_("Username already exists."))

        if not molo_profiles_forms.validate_no_email_or_phone(self.cleaned_data['username']):
            raise forms.ValidationError(
                _(
                    "Sorry, but that is an invalid username. Please don't use"
                    " your %s in your username." % validation_msg_fragment
                )
            )

        return self.cleaned_data['username']


class EditProfileForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Name"),
            }
        )
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Surname"),
            }
        )
    )
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                max_length=30,
            )
        ),
        label=_("Username"),
        error_messages={
            'invalid': _("This value must contain only letters, "
                         "numbers and underscores."),
        }
    )

    class Meta:
        model = UserProfile
        fields = [
            "alias", "date_of_birth", "mobile_number",
            "first_name", "last_name", "username"
        ]
