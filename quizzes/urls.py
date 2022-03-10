from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz, name="quiz"),
    path("<int:pk>/", views.take_quiz, name="take_quiz"),
    path("<int:pk>/submit/", views.submit_quiz_results, name="submit_quiz"),
]
