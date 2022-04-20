from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("profile/", include("accounts.urls")),
    path("auth/", include("allauth.urls")),
    path("questions/", include("questions.urls")),
    path("quiz/", include("quizzes.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
