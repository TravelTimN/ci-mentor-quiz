from django.db import models
from django.contrib.auth.models import User
from quizzes.models import Quiz


class Submission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, null=False, blank=False)
    duration = models.CharField(null=False, blank=False, max_length=10)
    taken = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    original_response = models.TextField(null=False, blank=False, default="")

    def __str__(self):
        return self.quiz.name


class Response(models.Model):
    # primarily for potential mentor inputs (fill-in-the-blank)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    answer = models.TextField(null=False, blank=False, default="")

    def __str__(self):
        return self.answer
