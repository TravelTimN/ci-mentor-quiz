from django.contrib import admin
from django.contrib.auth.models import User


# register custom list to showcase display_name instead of username
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "display_name", "email", "first_name", "last_name", "is_staff"
    )

    @admin.display()
    # show the display_name, not the username with uid attached
    def display_name(self, response):
        return response.profile.display_name


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
