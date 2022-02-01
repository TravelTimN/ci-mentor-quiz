from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_info, name="quiz"),
    path("<int:pk>/", views.take_quiz, name="take_quiz"),
    path("<int:pk>/save/", views.save_quiz_results, name="save_quiz"),
    path("<int:pk>/data/", views.quiz_data, name="quiz_data"),
]
