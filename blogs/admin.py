from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Админ-панель для публикаций блога."""

    list_display = ("id", "title", "author", "is_published", "created_at")
    list_filter = ("is_published", "author", "created_at")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "content", "author")}),
        ("Публикация", {"fields": ("is_published",)}),
        ("Даты", {"fields": ("created_at", "updated_at")}),
    )
