from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf import settings
from django.urls import path, re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^static/(?P<path>.*)$", views.serve),
]

admin.site.site_header = settings.PROJECT_NAME
