import re
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


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
    display_name = models.CharField(max_length=75, unique=False, null=False)
    taken_quiz = models.BooleanField(default=False, blank=False)
    mentor_type = models.CharField(choices=MENTOR_TYPE, max_length=40)
    resident_country = CountryField(
        blank_label="Country of Residence", null=False, blank=False)

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
    Signal to use the first+last names as the mentor's username.
    Strips-out any non-alphanumeric characters in names.
    Also applies a random [partial] uuid to the end of the username.
    If existing uuid exists on username, retain the same one.
    This all happens "pre_save".
    """
    if re.search(r"[a-zA-Z]+\-[a-zA-Z0-9]{5}", str(instance), re.I):
        uid = instance.username[-5:]
    else:
        uid = uuid.uuid4().hex[-5:]
    first = "".join(x for x in instance.first_name if x.isalnum()).lower()
    last = "".join(x for x in instance.last_name if x.isalnum()).lower()
    instance.username = f"{first}{last}-{uid}"  # johnsmith-abc09


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the mentor profile
    This happens "post_save".
    """
    # New users: create a new instance of a profile, with display_name
    if created:
        Profile.objects.create(
            user=instance,
            display_name=instance.username[:-6]
        )
    # Existing users: just save the profile
    instance.profile.save()
