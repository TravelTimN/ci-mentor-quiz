from django.contrib import admin
from .models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "quiz_type", "max_count", "is_active")  # table view
