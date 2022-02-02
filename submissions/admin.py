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
    list_display = ("id", "user", "taken", "quiz", "answer")  # table view

    @admin.display()
    # @admin.display() decorator allow list_display to use ForeignKeys
    def id(self, obj):
        return obj.submission.pk

    def user(self, obj):
        return obj.submission.user

    def taken(self, obj):
        return obj.submission.taken

    def quiz(self, obj):
        return obj.submission.quiz.name


admin.site.register(Submission, SubmissionAdmin)
