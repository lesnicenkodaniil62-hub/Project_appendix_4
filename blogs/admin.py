from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Админ-панель для модели BlogPost."""

    list_display = ("id", "title", "created_at", "is_published", "view_count")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
