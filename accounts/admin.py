from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "taken_quiz", "mentor_type")  # table view
    list_filter = ("taken_quiz", "mentor_type",)  # sidebar filter
    search_fields = ["user__username", "user__email",]  # search box
