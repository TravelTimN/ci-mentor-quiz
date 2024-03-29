import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from quizzes.models import Quiz
from submissions.models import Submission, Response, Attempt


@login_required
def profile(request):
    """ Display the user's profile. """
    user = get_object_or_404(User, username=request.user)
    # filter previous quiz submissions by user
    if request.user.is_superuser:
        user_submissions = Submission.objects.all().order_by("-taken")
        # get all quizzes for superuser, regardless of user-type or is_active
        quizzes = Quiz.objects.all()
    else:
        user_submissions = Submission.objects.filter(user=request.user)
        # get 'active' quiz(zes) for user-type
        quizzes = Quiz.objects.filter(
            quiz_type=user.profile.mentor_type, is_active=True
        )
    results = []
    for submission in user_submissions:
        attempts = Attempt.objects.filter(
            user=submission.user, quiz=submission.quiz).count()
        responses = Response.objects.filter(submission=submission.id)
        correct = responses.filter(is_correct="True").count()
        duration = str(datetime.timedelta(seconds=submission.duration))
        results.append({
            "quiz": submission,
            "answers": responses,
            "correct": correct,
            "questions": responses.count(),
            "percentage": submission.percent_correct,
            "duration": duration,
            "attempts": attempts,
        })

    template = "accounts/profile.html"
    context = {
        "user": user,
        "quizzes": quizzes,
        "results": results
    }

    return render(request, template, context)
