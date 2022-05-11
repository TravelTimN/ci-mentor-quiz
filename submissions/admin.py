from django.contrib import admin
from .models import Submission, Response
# from accounts.models import Profile


class ResponseInline(admin.TabularInline):
    model = Response


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = (
        "id", "username", "quiz", "duration",
        "taken", "percent_correct")  # table view
    list_filter = ("quiz", "user__profile__display_name")  # sidebar filter
    search_fields = ["user__email"]  # search box

    @admin.display()
    # @admin.display() decorator allow list_display to use FKs
    # list_display on Submission model cannot be "user" for customization
    def username(self, response):
        return response.user.profile.display_name


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "taken", "quiz", "correct")  # table view

    @admin.display()
    # @admin.display() decorator allow list_display to use FKs
    def id(self, response):
        return response.submission.id

    def user(self, response):
        return response.submission.user.profile.display_name

    def taken(self, response):
        return response.submission.taken

    def quiz(self, response):
        return response.submission.quiz.name

    def correct(self, response):
        return response.is_correct


admin.site.register(Submission, SubmissionAdmin)
