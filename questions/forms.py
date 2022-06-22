from django import forms
from django.forms import formset_factory
from .models import Question, Choice, Module, Subject
from quizzes.models import Quiz


class QuestionForm(forms.ModelForm):
    """
        Form to allow Admin to build a new Question on the DB.
    """
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            "required": True,
            "class": "form-control",
            "placeholder": "Question"
        })
    )
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        empty_label="Select Quiz",
        widget=forms.Select(attrs={
            "required": True,
            "class": "form-control",
        }),
    )
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        empty_label="Select Module",
        widget=forms.Select(attrs={
            "required": True,
            "class": "form-control",
        }),
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Select Subject",
        widget=forms.Select(attrs={
            "required": True,
            "class": "form-control",
        }),
    )
    type = forms.ChoiceField(
        choices=Question.QUESTION_TYPE,
        widget=forms.Select(attrs={
            "required": True,
            "class": "form-control",
        }),
    )
    optional_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "required": False,
            "class": "form-control",
            "placeholder": "Optional Helper Text",
            "rows": 2,
        })
    )

    class Meta:
        model = Question
        fields = "__all__"


class ChoiceForm(forms.ModelForm):
    choice = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Original Choice",
        })
    )

    class Meta:
        model = Choice
        fields = ("choice", "correct_answer",)


# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
# https://stackoverflow.com/a/5479472
# allow dynamic addition of new Question Choices
ChoiceFormSet = formset_factory(
    ChoiceForm, extra=0, min_num=1, max_num=10, can_delete=True)
