import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Quiz
from questions.models import Question


def quiz_info(request):
    user = get_object_or_404(User, username=request.user)
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/info.html", {"user": user, "quizzes": quizzes})


def take_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quizzes/quiz.html", {"quiz": quiz})


def quiz_data(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for question in quiz.get_questions():
        choices = []
        for choice in question.get_choices():
            choices.append(choice.choice)
        questions.append({"question": str(question), "choices": choices, "type": question.type})
    return JsonResponse({"data": questions, })


def save_quiz_results(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    questions = []
    for key in data.keys():
        print(key)
        current_question = Question.objects.get(question=key)
        questions.append(current_question)
    # questions.models.Question.DoesNotExist: Question matching query does not exist.
    # https://github.com/TravelTimN/ci-mentor-quiz/issues/1
    print(questions)
    return JsonResponse({"text": "works"})
