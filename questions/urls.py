from django.urls import path
from . import views

urlpatterns = [
    path("", views.questions, name="questions"),
    path("add/", views.add_question, name="add_question"),
    path("update/<int:id>", views.update_question, name="update_question"),
]
