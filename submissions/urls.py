from django.urls import path
from . import views

urlpatterns = [
    path("ajax_quiz_start/", views.ajax_quiz_start, name="ajax_quiz_start"),
]
