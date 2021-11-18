from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request, username):
    """ Display the user's profile. """
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
        else:
            messages.error(
                request,
                ("Update failed. Please ensure the form is valid."))
    else:
        form = UserProfileForm(instance=user_profile)

    template = "accounts/profile.html"
    context = {
        "form": form,
    }

    return render(request, template, context)
