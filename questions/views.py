from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from questions.models import Question, Choice


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
