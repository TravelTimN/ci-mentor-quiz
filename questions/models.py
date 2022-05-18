from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from quizzes.models import Quiz


class Module(models.Model):
    # LMS module selection
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        """
        sort by id
        """
        ordering = ["id"]

    def __str__(self):
        return self.name.replace("_", " ")


class Subject(models.Model):
    # course subject (HTML, JS, Flask, Django, etc.)
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        """
        sort by id
        """
        ordering = ["id"]

    def __str__(self):
        return self.name.replace("_", " ")


class Question(models.Model):
    # multi-choice, input, integer, true/false, short answer, url
    QUESTION_TYPE = [
        (None, "Quiz Type"),
        ("checkbox", "Checkbox"),
        ("text", "Input"),
        ("number", "Number"),
        ("radio", "Radio"),
        ("textarea", "Textarea"),
        ("url", "URL"),
    ]
    question = models.CharField(max_length=200, blank=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    type = models.CharField(choices=QUESTION_TYPE, max_length=10)
    optional_text = models.TextField(null=True, blank=True)

    class Meta:
        """
        sort by id
        """
        ordering = ["id"]

    def __str__(self):
        return self.question

    def get_choices(self):
        return self.choice_set.all()


class Choice(models.Model):
    choice = models.CharField(max_length=100, null=False, blank=False)
    correct_answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice
