from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from quizzes.models import Quiz


class Module(models.Model):
    # LMS module selection
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Subject(models.Model):
    # course subject (HTML, JS, Flask, Django, etc.)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    # question types (multiple choice, true/false, short-answer)
    QUESTION_TYPE = [
        ("multi", "Multiple Choice"),
        ("bool", "True or False"),
        ("short", "Short Answer"),
    ]
    question = models.CharField(max_length=200, blank=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    type = models.CharField(choices=QUESTION_TYPE, max_length=10)

    def __str__(self):
        return f"{self.pk}: {self.question}"

    def get_choices(self):
        return self.answer_set.all()


class Choice(models.Model):
    choice = models.CharField(max_length=100, null=True)
    correct_answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice
