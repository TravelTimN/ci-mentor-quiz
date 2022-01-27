from django.contrib import admin
from .models import Submission, Response


class ResponseInline(admin.TabularInline):
    model = Response


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ("user", "quiz", "duration", "taken")  # table view
    list_filter = ("quiz",)  # sidebar filter


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("submission", "answer")  # table view


admin.site.register(Submission, SubmissionAdmin)
