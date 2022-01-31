from django.contrib import admin
from .models import Question, Choice, Module, Subject


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question", "quiz", "module", "subject", "type")  # table view
    list_filter = ("quiz", "type", "subject", "module",)  # sidebar filter
    search_fields = ["question", "module", "subject", "type"]  # search box


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice", "correct_answer")  # table view


admin.site.register(Question, QuestionAdmin)
admin.site.register(Module)
admin.site.register(Subject)
