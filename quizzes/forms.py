from django import forms
from .models import Quiz


class QuizForm(forms.ModelForm):
    """
        Form to allow Admin to build a new Quiz on the DB.
    """
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "required": True,
            "class": "form-control",
            "placeholder": "Quiz Name"
        })
    )
    quiz_type = forms.ChoiceField(
        choices=Quiz.QUIZ_TYPE,
        widget=forms.Select(attrs={
            "required": True,
            "class": "form-control",
        }),
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            "required": True,
            "class": "form-control",
            "placeholder": "Description of the quiz"
        })
    )
    max_count = forms.CharField(
        widget=forms.TextInput(attrs={
            "required": True,
            "class": "form-control",
            "placeholder": "Maximum Number of Questions"
        })
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            "required": False,
            "class": "form-check-input mt-0 mx-2",
        }),
    )

    class Meta:
        model = Quiz
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # is_active isn't a required field
        self.fields["is_active"].required = False

        # generate list of available Quiz Types
        self.fields["quiz_type"].choices = [["", "Select Quiz Type"]]
        qtypes = Quiz.QUIZ_TYPE
        for qtype in qtypes:
            self.fields["quiz_type"].choices.append(qtype)
