from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from allauth.account.forms import LoginForm, SignupForm


class CustomSignupForm(SignupForm):
    """
    Override of the default allauth signup form.
    This will allow custom attributes (eg: class, placeholder)
    """
    first_name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )
    last_name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )

    class Meta:
        model = UserProfile
        fields = ["__all__"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override class and placeholder attributes
        self.fields["email"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Email"},
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Password"},
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Confirm Password"},
        )


class CustomLoginForm(LoginForm):
    """
    Override of the default allauth login form.
    This will allow custom attributes (eg: class, placeholder)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override class and placeholder attributes
        self.fields["login"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Email"},
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Password"},
        )
