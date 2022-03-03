from django.db import models
from django.contrib.auth.models import User
from quizzes.models import Quiz
from questions.models import Question


class Submission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False, default="0")
    taken = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    original_response = models.JSONField(null=False, blank=False)
    percent_correct = models.IntegerField(null=False, blank=False, default="0")

    def __str__(self):
        return self.quiz.name


class Response(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    correct_answer = models.CharField(null=False, max_length=999, default="")
    user_answer = models.CharField(null=False, max_length=9999, default="")
    time_taken = models.IntegerField(null=False, blank=False, default="0")

    def __str__(self):
        return f"User: {self.submission.user} | QID: {self.question} | Correct: {self.is_correct}"
