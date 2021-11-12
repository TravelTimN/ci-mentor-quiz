from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import CustomLoginForm, CustomSignupForm


# def register(request):
#     if request.method == "POST":
#         reg_form = UserRegistrationForm(request.POST)

#         # Ensure form validations are met
#         if reg_form.is_valid():
#             user = reg_form.save()
#             auth.login(request, user)
#             messages.success(request, 'You are now registered & logged in.')
#             return redirect('index')

#     elif request.user.is_authenticated:
#         messages.error(request, 'You are logged in already!')
#         return redirect(request, 'index')
#     else:
#         reg_form = UserRegistrationForm()

#     context = {
#         'register_page': 'active',
#         'form': reg_form
#     }
#     return render(request, 'accounts/register.html', context)
