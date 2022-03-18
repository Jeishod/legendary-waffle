from django.contrib import admin

from data.models import File, Project, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "is_superuser",
        "created_at",
        "updated_at",
        "archived_at",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "created_at",
        "updated_at",
        "archived_at",
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "owner",
        "created_at",
        "updated_at",
        "archived_at",
    )
