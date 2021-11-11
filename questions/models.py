from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Subject(models.Model):
    # course subject (HTML, JS, Flask, Django, etc.)
    name = models.CharField(max_length=100, blank=False)
    friendly_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Module(models.Model):
    # LMS module selection
    name = models.CharField(max_length=100, blank=False)
    friendly_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Question(models.Model):
    # question bank
    question = models.CharField(max_length=100, blank=False)
    opt1 = models.CharField(max_length=50, blank=False)
    opt2 = models.CharField(max_length=50, blank=False)
    opt3 = models.CharField(max_length=50, blank=True)
    opt4 = models.CharField(max_length=50, blank=True)
    opt5 = models.CharField(max_length=50, blank=True)
    answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    subject = models.ForeignKey("Subject", null=True, blank=True, on_delete=models.SET_NULL)
    module = models.ForeignKey("Module", null=True, blank=True, on_delete=models.SET_NULL)
