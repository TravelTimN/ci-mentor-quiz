from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining
    mentor information and quiz history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taken_quiz = models.BooleanField(default=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user.first_name
