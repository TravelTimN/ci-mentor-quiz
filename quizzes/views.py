from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Quiz


def quiz_info(request):
    user = get_object_or_404(User, username=request.user)
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/info.html", {"user": user, "quizzes": quizzes})


def take_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quizzes/quiz.html", {"quiz": quiz})
