from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404, handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("profile/", include("accounts.urls")),
    path("auth/", include("allauth.urls")),
    path("questions/", include("questions.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("submissions/", include("submissions.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main.views.handler404"
handler500 = "main.views.handler500"
