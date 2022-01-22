from django.shortcuts import get_object_or_404, render  # , redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from .models import Profile
# from .forms import UserUpdateForm


# @login_required
# def profile(request):
#     """ Display the user's profile. """
#     user = get_object_or_404(User, username=request.user)

#     if request.method == "POST":
#         form = UserUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile successfully updated")
#         else:
#             messages.error(
#                 request,
#                 ("Update failed. Please ensure the form is valid."))
#     else:
#         form = UserUpdateForm(instance=user)

#     template = "accounts/profile.html"
#     context = {
#         "form": form,
#     }

#     return render(request, template, context)


@login_required
def profile(request):
    """ Display the user's profile. """
    # NO USE OF 'User' model, form simply using 'request.user' default

    # user = get_object_or_404(User, username=request.user)

    template = "accounts/profile.html"
    context = {}

    return render(request, template, context)
