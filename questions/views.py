from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm, ChoiceFormSet


@login_required
def questions(request):
    """ Grab all questions for Admin management """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    questions = Question.objects.all()
    questions_choices = []
    for question in questions:
        choices = []
        for choice in question.get_choices():
            choices.append(choice.choice)
        questions_choices.append({
            "id": question.pk,
            "quiz": question.quiz.name,
            "question": str(question),
            "module": question.module,
            "subject": question.subject,
            "type": question.type,
            "choices": choices,
        })

    template = "questions/questions.html"
    context = {
        "questions": questions_choices,
    }
    return render(request, template, context)


@login_required
def add_question(request):
    """ Allow admins to create new Questions/Choices on the DB """
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    question_form = QuestionForm(request.POST or None)
    choice_form_set = ChoiceFormSet(request.POST or None)

    if request.method == "POST":
        if question_form.is_valid and choice_form_set.is_valid:
            # save the Question model
            qform = question_form.save()
            # loop each instance of the FormSet and save each "Choice"
            for choice in choice_form_set:
                choice.instance.question = qform  # set FK to Question above
                choice.save()
            messages.success(request, "Question/Choices successfully added!")
            return redirect(update_question, qform.pk)
        else:
            messages.error(request, "An error has occurred. Please try again.")

    # non-POST (GET) method, or if form is not valid, it will retain form data
    question_form = QuestionForm()
    choice_form_set = ChoiceFormSet()

    template = "questions/add_question.html"
    context = {
        "question_form": question_form,
        "choice_form_set": choice_form_set,
    }
    return render(request, template, context)


@login_required
def update_question(request, id):
    """ Admin management of existing Question/Choices """
    # TODO: ------------------
    # TODO: WORK IN PROGRESS
    # TODO: ------------------
    if not request.user.is_superuser:
        # user is not superuser; take them to their profile
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("profile"))
    # is superuser
    question = get_object_or_404(Question, id=id)
    choices = []
    for choice in question.get_choices():
        choices.append(choice.choice)

    template = "questions/update_question.html"
    context = {
        "question": question,
        "choices": choices,
    }
    return render(request, template, context)
