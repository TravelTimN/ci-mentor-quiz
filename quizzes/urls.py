from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz, name="quiz"),
    path("manage/", views.quizzes, name="quizzes"),
    path("add/", views.add_quiz, name="add_quiz"),
    path("update/<int:pk>/", views.update_quiz, name="update_quiz"),
    path("delete/<int:pk>/", views.delete_quiz, name="delete_quiz"),
    path("<int:pk>/", views.take_quiz, name="take_quiz"),
    path("<int:pk>/submit/", views.submit_quiz_results, name="submit_quiz"),
]
