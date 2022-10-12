from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Attempt, Submission


@login_required
def ajax_quiz_start(request):
    """
    User has clicked the 'Start Quiz' button.
    AJAX call to submit new 'Attempt' model.
    This is to see how often a user is revisiting the quiz.
    Some potential mentors have submitted the entire quiz in 2mins.
    Likely reviewed the questions first, then copy/pasted in the form.
    """
    user = get_object_or_404(User, username=request.user)
    if request.is_ajax():
        attempt = Attempt.objects.create(user=user)
        return HttpResponse("AJAX Success")
    else:
        return redirect("profile")


@login_required
def delete_submission(request, pk):
    """
    Superusers can delete an entire quiz submission and results
    """
    if not request.user.is_superuser:
        messages.error(request, "Access Denied. Invalid Permissions.")
        return redirect("profile")
    submission = get_object_or_404(Submission, id=pk)
    messages.success(request, "Submission successfully deleted")
    submission.delete()
    return redirect("profile")
