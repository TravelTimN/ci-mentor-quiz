from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries import countries
from allauth.account.forms import LoginForm, SignupForm
from .models import Profile


class CustomSignupForm(SignupForm):
    """
    Override of the default allauth signup form.
    This will allow custom attributes (eg: class, placeholder)
    """
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )
    resident_country = CountryField(
        blank=False).formfield(
            widget=forms.Select(attrs={"class": "form-control"}))
    mentor_type = forms.ChoiceField(
        required=True,
        choices=Profile.MENTOR_TYPE,
        widget=forms.RadioSelect()
    )

    class Meta:
        """
        ModelSerializer for displaying
        'all' fields on the admin dashboard
        """
        model = Profile
        fields = ["__all__"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resident_country"].choices = [
            ["", "Country of Residence"]
        ]
        for country in countries:
            self.fields["resident_country"].choices.append(country)

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

        # set first_name to be autofocs on page load
        self.fields["first_name"].widget.attrs["autofocus"] = True

    # override the user's profile fields on registration
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.profile.resident_country = self.cleaned_data["resident_country"]
        user.profile.mentor_type = self.cleaned_data["mentor_type"]
        user.save()
        return user


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
