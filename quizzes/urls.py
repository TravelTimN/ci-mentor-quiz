from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_info, name="quiz"),
    path("<int:pk>/", views.take_quiz, name="take_quiz"),
]
