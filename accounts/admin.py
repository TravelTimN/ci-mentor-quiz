from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "taken_quiz")  # table view
    list_filter = ("taken_quiz",)  # sidebar filter
    search_fields = ["user", "taken_quiz"]  # search box
