import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Quiz
from questions.models import Question


def quiz_info(request):
    user = get_object_or_404(User, username=request.user)
    quizzes = Quiz.objects.all()

    template = "quizzes/info.html"
    context = {
        "user": user,
        "quizzes": quizzes,
    }

    return render(request, template, context)


def take_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)

    template = "quizzes/quiz.html"
    context = {
        "quiz": quiz,
    }

    return render(request, template, context)


def quiz_data(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for question in quiz.get_questions():
        choices = []
        for choice in question.get_choices():
            choices.append(choice.choice)
        questions.append({
            "id": question.pk, "question": str(question),
            "choices": choices, "type": question.type
        })
    return JsonResponse({"data": questions, })


def save_quiz_results(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    questions = []
    for key in data.keys():
        current_question = Question.objects.get(id=key.replace("q", ""))
        questions.append(current_question)
    print(questions)
    return JsonResponse({"text": "works"})
