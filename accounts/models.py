from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    A user profile model for maintaining
    mentor information and quiz history
    """
    # mentor type choices
    MENTOR_TYPE = [
        ("is_mentor", "I am a Code Institute Mentor"),
        ("is_not_mentor", "I want to be a Code Institute Mentor"),
    ]

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    taken_quiz = models.BooleanField(default=False, blank=False)
    mentor_type = models.CharField(choices=MENTOR_TYPE, max_length=40)

    class Meta:
        """
        Sort all users in the admin dashboard
        by their usernames, alphabetically
        """
        ordering = ["user__username"]

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=User)
def update_username_from_name(sender, instance, **kwargs):
    """
    Signal to use the first+last names as the mentor's username
    Strips-out any non-alphanumeric characters in names (\'\s\- etc)
    This happens "pre_save".
    """
    username = instance.first_name + instance.last_name
    instance.username = "".join(x for x in username if x.isalnum()).lower()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the mentor profile
    This happens "post_save".
    """
    # New users: create a new instance of a profile
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()
