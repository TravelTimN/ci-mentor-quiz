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
    list_display = ("choice", "get_question", "correct_answer", "id")  # table view
    list_filter = ("question__quiz",)  # sidebar filter

    @admin.display()
    def get_question(self, response):
        return response.question.question[:50]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Module)
admin.site.register(Subject)
