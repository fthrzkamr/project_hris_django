from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth_web.urls")),
    path("", include("core.urls")),
]
