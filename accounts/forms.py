from django import forms
from django.contrib.auth.models import User
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

    # override the profile's "mentor_type" field on registration
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
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


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         """
#         Instance of Django's User Model for users to edit their profile,
#         and which fields to include/exclude
#         """
#         model = User
#         fields = ["first_name", "last_name", "email", "username"]
#         help_texts = {
#             "email": None,
#             "username": None,
#         }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         """
#         Instance of custom Profile Model for users to edit their profile,
#         and which fields to include/exclude
#         """
#         model = Profile
#         exclude = ("taken_quiz",)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
