from django.conf import settings
from django.db import models


class Category(models.Model):
    """Модель категории товара."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Введите название товара",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание товара",
    )
    image = models.ImageField(
        upload_to="photos/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию товара",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену товара",
    )

    # Владелец товара
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Владелец",
        help_text="Пользователь, создавший товар",
    )

    # Статус публикации (False = не опубликовано)
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Если отмечено — товар виден всем пользователям",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self) -> str:
        return self.name
