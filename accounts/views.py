import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from quizzes.models import Quiz
from submissions.models import Submission, Response


@login_required
def profile(request):
    """ Display the user's profile. """
    user = get_object_or_404(User, username=request.user)
    # get the ID of this user's specific quiz-type
    quiz_id = Quiz.objects.filter(
        name=user.profile.mentor_type).values_list("id", flat=True)[:1][0]
    # filter previous quiz submissions by user
    if request.user.is_superuser:
        user_submissions = Submission.objects.all()
    else:
        user_submissions = Submission.objects.filter(user=request.user)
    results = []
    for submission in user_submissions:
        responses = Response.objects.filter(submission=submission.id)
        correct = responses.filter(is_correct="True").count()
        duration = str(datetime.timedelta(seconds=submission.duration))
        results.append({
            "quiz": submission,
            "answers": responses,
            "correct": correct,
            "questions": responses.count(),
            "percentage": submission.percent_correct,
            "duration": duration
        })

    template = "accounts/profile.html"
    context = {
        "user": user,
        "quiz_id": quiz_id,
        "results": results
    }

    return render(request, template, context)
