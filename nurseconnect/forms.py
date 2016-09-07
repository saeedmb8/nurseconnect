from django import forms
from django.utils.translation import ugettext_lazy as _
from molo.profiles.forms import EditProfileForm
from molo.profiles.models import UserProfile


class NurseConnectEditProfileForm(EditProfileForm):
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
