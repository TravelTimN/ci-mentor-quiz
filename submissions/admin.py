from django.contrib import admin
from .models import Submission, Response


class ResponseInline(admin.TabularInline):
    model = Response


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ("user", "quiz", "duration", "taken")  # table view
    list_filter = ("quiz", "user")  # sidebar filter
    search_fields = ["user__email"]  # search box


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "taken", "quiz", "correct")  # table view

    @admin.display()
    # @admin.display() decorator allow list_display to use ForeignKeys
    def id(self, response):
        return response.question.pk

    def user(self, response):
        return response.submission.user

    def taken(self, response):
        return response.submission.taken

    def quiz(self, response):
        return response.submission.quiz.name

    def correct(self, response):
        return response.is_correct


admin.site.register(Submission, SubmissionAdmin)
