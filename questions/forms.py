from django import forms
from django.forms import formset_factory
from .models import Question, Choice, Module, Subject
from quizzes.models import Quiz


class QuestionForm(forms.ModelForm):
    """
        Form to allow Admin to build a new Question on the DB.
    """
    question = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Question"
        })
    )
    quiz = forms.ModelChoiceField(
        required=True,
        queryset=Quiz.objects.all(),
        empty_label="Select Quiz",
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
    )
    module = forms.ModelChoiceField(
        required=True,
        queryset=Module.objects.all(),
        empty_label="Select Module",
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
    )
    subject = forms.ModelChoiceField(
        required=True,
        queryset=Subject.objects.all(),
        empty_label="Select Subject",
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
    )
    type = forms.ChoiceField(
        required=True,
        choices=Question.QUESTION_TYPE,
        widget=forms.Select(attrs={
            "class": "form-control",
        }),
    )
    optional_text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Optional Helper Text",
            "rows": 2,
        })
    )

    class Meta:
        model = Question
        fields = "__all__"


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        # choice, correct_answer, question
        # fields = "__all__"
        fields = ("choice", "correct_answer",)


# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
# https://stackoverflow.com/a/5479472
# allow dynamic addition of new Question Choices
ChoiceFormSet = formset_factory(ChoiceForm, extra=1, max_num=10)
