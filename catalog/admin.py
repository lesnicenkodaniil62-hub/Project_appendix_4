from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий."""

    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для товаров."""

    list_display = ("id", "name", "price", "category", "owner", "is_published", "created_at")
    list_filter = ("category", "is_published", "owner")
    search_fields = ("name", "description")
    list_editable = ("is_published",)  # Можно менять статус прямо в списке

    fieldsets = (
        (None, {"fields": ("name", "description", "price", "category", "image")}),
        (
            "Публикация и владелец",
            {"fields": ("owner", "is_published")},
        ),
        (
            "Даты",
            {"fields": ("created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at")
