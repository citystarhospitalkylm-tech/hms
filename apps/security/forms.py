# apps/security/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RoleAuthenticationForm(AuthenticationForm):
    """
    Extends AuthenticationForm with custom labels
    and a check that the user has a role.
    """

    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Enter your username"
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password"
        })
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. "
            "Note that both fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
        "no_role": _("You don’t have a role assigned. Please contact support."),
    }

    def confirm_login_allowed(self, user):
        # Run Django’s default checks first
        super().confirm_login_allowed(user)

        # Now enforce “user.role” presence
        if not hasattr(user, "role") or not user.role:
            raise forms.ValidationError(
                self.error_messages["no_role"],
                code="no_role",
            )