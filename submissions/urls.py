from django.urls import path
from . import views

urlpatterns = [
    path("ajax_quiz_start/", views.ajax_quiz_start, name="ajax_quiz_start"),
    path(
        "delete_submission/<int:pk>/",
        views.delete_submission, name="delete_submission"),
]
